#!/usr/bin/env sh

# Copyright (C) 2018-2022 Brandon Zorn <brandonzorn@cock.li>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# SCRIPT INFO
# 3.1.0
# 2019-02-09


#ZFS Builtin Kernel Build Script - gentoo

#hard requirments
#>=linux-4.17.0 : >=zfs-0.8.0 / git | 1.x.x script for previous support

#storage dirs - need to exist
#${XDG_DATA_DIRS}/kernel/{config,distfiles,src}

#assumptions
#/usr/src/linux is real source or symlink to real source
#$run_kernel_bump is based om my own config and others CONFIG_* options may be needed based on kenrel config

###What this script does, basically###

###if no preconfigured sources exist for ebuild sys-fs/zfs-kmod###
#runs configure phase on sys-fs/zfs-kmod ebuild
#saves work/ to tar.zst file in $kmod_src
#installs configured kmod-zfs to /usr/src/linux
#build kernel

###if preconfigured sources exist for ebuild sys-fs/zfs-kmod###
#moves saved work in tar.zst file to /usr/src/linux
#build kernel

#TODO
#add comments for all niche cases in script
#multi build kernels
#	multi kernel build - debug and regular, from one invocation
#	single build, either debug or regular

die()
{
	/bin/echo -e "\033[0;31m$*\033[m"
	if [ "${print_vars}" = "1" ];then
		read -r -p "Press enter to print all vars. " X;unset X
		set
	fi
	exit 1
}

if [ "$(id -u)" -ne 0 ];then die "Requires root";fi

finish(){ if [ -d "${tmpdir}" ];then rm --preserve-root -r "${tmpdir}";fi; }
trap 'exit 1' INT HUP QUIT TERM USR1
trap finish EXIT
tmpdir=$(mktemp -d)
chmod 755 "${tmpdir}"

msc(){ ${kmake} syncconfig; }
cdkdir(){ cd "${kdir}" || die "ERROR: can not cd into kenrel directory"; }

storage="${XDG_DATA_HOME}/kernel"
settings="${XDG_CONFIG_HOME}/kernel/config"

ksym="/usr/src/linux"
kdir="$(readlink -f "${ksym}")"

cc_use_clang="0"

clean_kernel_src="1"

use_zfs_version="git"

run_emerge="0"
run_kmod_build="0"

run_intro="1"
run_zfs_build="1"
run_kernel_post="1"
run_kernel_build="1"
run_kernel_install="1"

print_vars="0"
intro_extra="0"
force_bump_check="0"

use_distdir="1"

use_modules="0"
use_local_zfs_ebuild="0"

if [ -f "${settings}" ];then
	. "${settings}"
else
	if ! [ -d "${storage}" ];then
		mkdir "${storage}"
	fi
	printf "Creating config file at ${settings}\n"
	printf "#!/usr/bin/env sh\n" >| "${settings}"
	printf "use_zfs_version=\"release\"\n" >> "${settings}"

	exit
fi

while getopts "RBCEDGbdgrceIimplxzvh" OPT;do
	case "$OPT" in
		G) cc_use_clang="1";;
		D) print_vars="1";;
		B) run_kernel_bump="1";force_bump_check="1";;
		b) run_kernel_bump="0";force_bump_check="1";;
		d) use_distdir="0";;
		c) run_kmod_build="1";;
		e) run_emerge="1";;
		g) use_zfs_version="git";;
		I) run_intro="0";;
		i) run_kernel_install="0";run_kernel_post="0";;
		l) use_local_zfs_ebuild="1";;
		p) run_kernel_post="0";;
		m) use_modules="1";;
		r) use_zfs_version="release";;
		x) run_zfs_build="0";;
		v) intro_extra="1";;
		z) run_zfs_build="1";run_kernel_build="0";;
		C) clean_kernel_src="0";;
		R) rm "${settings}";exit;;
		E) ${EDITOR} "${settings}";exit;;
		h)
			printf "DEBUG\n"
			printf " -D\tIf script exits with die() print all shell variables\n"
			printf "\nGENERAL\n"
			printf " -b\tforce run_kernel_bump=0\n"
			printf " -B\tforce run_kernel_bump=1\n"
			printf " -E\tEdit config file\n"
			printf " -h\tprint this help\n"
			printf " -I\tdisable intro\n"
			printf " -R\treset config file and exit\n"
			printf " -v\tprint extra vars in intro\n"
			printf "\nZFS\n"
			printf " -c\tbuild kmod even if preconfigured sources exist\n"
			printf " -d\tuse \$XDG_DATA_DIR/kenrel/distfiles as \$DISTDIR, does not work with FEATURES=userfetch\n"
			printf " -g\tuse git ebuild\n"
			printf " -r\tuse release ebuild\n"
			printf " -l\tuse local repo in \$PORTDIR_OVERLAY\n"
			printf "\nKERNEL BUILDING\n"
			printf " -G\tbuild kernel using clang\n"
			printf " -C\tdisable cleaning kernel source dir\n"
			printf " -e\tenable running emerge in post\n"
			printf " -i\tbuild kernel but do not install or run post, implies -p\n"
			printf " -m\tforce enable module build\n"
			printf " -p\tdisable post, emerge, initramfs, and grub configure\n"
			printf " -x\tdisable zfs build, all zfs checks must still pass, becomes fancy 'make;make install'\n"
			printf " -z\tonly run zfs build, will install zfs into kenrel tree\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

if ! [ -f "${kdir}/.config" ];then
	die "ERROR: no config in kenrel directory"
fi

if [ "${cc_use_clang}" = "1" ];then
	#ld.lld only works when clang is the compiler otherwise fails with
	#error: init sections too big!
	CC="clang"
	LD="ld.lld"
else
	#force bfd since gold is not supported
	#https://bugs.gentoo.org/694612
	#https://bugzilla.kernel.org/show_bug.cgi?id=204951
	CC="gcc"
	LD="ld.bfd"
fi
kmake="nice -19 make -j$(($(nproc)*2+1)) -l$(($(nproc)+1)) CC=${CC} LD=${LD}"

if [ "${use_modules}" = "0" ];then
	if [ "$(grep CONFIG_MODULES=y "${kdir}/.config")" ];then
		use_modules="1"
	fi
fi

if ! [ -e "${ksym}" ];then
	die "ERROR: ${ksym} is not a valid symlink"
fi
if ! [ -d "${storage}/config" ];then
	mkdir -p "${storage}/config"
fi

kver_full="$(echo "${kdir##*/linux-}")"
case "$(echo "${kdir##*/}"|grep rc)" in
	*rc*) #rc kernel
		kver="$(echo "${kver_full}"|sed s'/.$//')"
		;;
	*) #release kernel
		kver="$(echo "${kver_full}"|awk 'BEGIN{FS=OFS="."} NF--')"
		;;
esac

switch_kconf="${storage}/config/${kver}-config"
if [ "${force_bump_check}" = "0" ];then #allows flags to overwrite
	if [ -f "${switch_kconf}" ];then
		run_kernel_bump="0"
	else
		run_kernel_bump="1"
	fi
fi

#CONFIG_MODULES and CONFIG_KALLSYMS are required to build kmod
#which are not needed at runtime if zfs is build into the kernel.
while [ "${run_kernel_bump}" = "1" ];do
	if ! [ -f "${switch_kconf}" ];then
		cp "${kdir}/.config" "${switch_kconf}"
	fi
	c1=$(grep -s CONFIG_MODULES=y "${switch_kconf}")
	c2=$(grep -s CONFIG_KALLSYMS=y "${switch_kconf}")
	if [ "${run_zfs_build}" = "1" ] && [ -z "${c1}" ] || [ -z "${c2}" ];then
		printf "\nRequired option[s] located at:\n"
		if [ -z "${c1}" ];then
			printf "\n[*] Enable loadable module support\n"
		fi
		if [ -z "${c2}" ];then
			printf "\nGeneral setup  --->\n"
			printf "\t[*] Configure standard kernel features (expert users)  --->\n"
			printf "\t\t[*] Load all symbols for debugging/ksymoops\n\n"
		fi
		read -p "Enter to config switch config: " z;unset z
		if [ -f "${switch_kconf}" ];then
			rm "${switch_kconf}"
		fi
		cdkdir
		${kmake} nconfig
		cp .config "${switch_kconf}"
	else
		break
	fi
done

#repo locations
#https://github.com/thermitegod/etc-portage/tree/master/repos.conf
if [ "${use_local_zfs_ebuild}" = "0" ];then
	repo_conf="gentoo.conf"
else
	repo_conf="local.conf"
fi
port="$(grep location "/etc/portage/repos.conf/${repo_conf}"|head -n1|awk '{print $3}')"

if [ "${use_zfs_version}" = "release" ];then
	Z="$(ls -1A --ignore=*9999* "${port}/sys-fs/zfs-kmod"|sort -V|tail -n1)"
	zver="$(echo "${Z%%.ebuild}"|sed 's/^.\{9\}//')" #clean up filename
	kmod="zfs" #build path
	if [ "${use_distdir}" = "0" ];then
		#keep sources on eclean-dist
		export DISTDIR="${storage}/distfiles"
	fi
else
	#git version
	zver="9999"
	kmod="zfs-kmod" #build path
fi

if ! [ -f "${port}/sys-fs/zfs-kmod/zfs-kmod-${zver}.ebuild" ];then
	die "ERROR: missing zfs-kmod-${zver}.ebuild"
fi

kmod_src="${storage}/src/${kver}/${zver}"
if ! [ -d "${kmod_src}" ] && [ "${run_zfs_build}" = "1" ];then
	#need to build if configured src do not exists
	run_kmod_build="1"
fi

if [ "${run_intro}" = "1" ];then
	printf "kernel             : %s\n" "${kdir}"
	printf "compiler/linker    : %s\n" "${CC}/${LD}"
	printf "Install Kernel     : %s\n" "${run_kernel_install}"
	printf "ZFS version        : %s\n" "${zver}"
	printf "ZFS local ebuild   : %s\n" "${use_local_zfs_ebuild}"
	printf "Configure kmod     : %s\n" "${run_kmod_build}"
	printf "Enable modules     : %s\n" "${use_modules}"
	printf "Running emerge     : %s\n" "${run_emerge}"
	if [ "${intro_extra}" = "1" ];then
		printf "\nEXTRA\n"
		printf "Make command       : %s\n" "${kmake}"
		printf "PORTDIR            : %s\n" "${port}"
		printf "kver               : %s\n" "${kver}"
		printf "kver_full          : %s\n" "${kver_full}"
		printf "Tempdir            : %s\n" "${tmpdir}"
		printf "\n"
		eselect kernel list
	fi
	printf "\n"
	read -p "Enter to start kernel build " z;unset z
fi

if [ "${run_zfs_build}" = "1" ];then
	zver_path="${zver}"

	if [ "$(echo "${zver}"|grep rc)" ];then
		zver="${zver%%_rc*}" #rc ebuilds
	fi
	if [ "$(echo "${zver}"|grep "\-r")" ];then
		zver="${zver%%-r*}" #rev bump ebuilds
	fi
	archive="zfs-${zver}.tar.zst"

	if [ "${run_kmod_build}" = "1" ];then
		cdkdir
		msc
		if [ "${use_modules}" = "0" ];then
			mv .config "${tmpdir}"
			cp "${switch_kconf}" .config
		fi
		#${kmake} prepare #FIXME does not work if CC=clang
		make CC=gcc LD=ld.bfd prepare

		export PORTAGE_TMPDIR="${tmpdir}"
		if [ -d "${kmod_src}" ];then
			rm --preserve-root -r "${kmod_src}"
		fi
		mkdir -p "${kmod_src}"
		EXTRA_ECONF="--with-linux=${kdir} --enable-linux-builtin" \
			ebuild "${port}/sys-fs/zfs-kmod/zfs-kmod-${zver_path}.ebuild" configure
		cd "${tmpdir}/portage/sys-fs/zfs-kmod-${zver_path}/work/${kmod}-${zver}" || die
		./copy-builtin "${kdir}" || die "ERROR: copy-builtin failed"
		cd .. || die
		tar -cf - "${kmod}-${zver}" -P | zstd -T0 -4 >| "${archive}" || die "ERROR: did not compress zfs work dir"
		mv "${archive}" "${kmod_src}"

		if [ "${use_modules}" = "0" ];then
			rm "${kdir}/.config"
			mv "${tmpdir}/.config" "${kdir}"
		fi

		if [ "${cc_use_clang}" = "1" ];then
			kernel-clean-src -c
		fi
	else
		cd "${kmod_src}" || die
		tar -I zstd -xf "${archive}" -C "${tmpdir}" || die "ERROR: cannot extract zfs work dir"
		cd "${tmpdir}/${kmod}-${zver}" || die
		./copy-builtin "${kdir}" || die "ERROR: copy-builtin failed"
	fi
fi

if [ "${run_kernel_build}" = "1" ];then
	cdkdir
	msc
	${kmake} || die "ERROR: kernel build failed"
	if [ "${run_kernel_install}" = "1" ];then
		if [ "${use_modules}" = "1" ];then
			${kmake} modules_install
		fi
		${kmake} install
	fi

	if [ "${run_kernel_post}" = "1" ];then
		if [ "${run_emerge}" = "1" ];then
			emerge_cmd="emerge --ignore-default-opts --oneshot --quiet"
			if [ "${run_kmod_build}" = "1" ];then
				if [ "${use_zfs_version}" = "release" ];then
					emerge --ignore-default-opts --oneshot --quiet --update sys-fs/zfs
				else
					#will always rebuild zfs when using git
					emerge --ignore-default-opts --oneshot --quiet sys-fs/zfs
				fi
			fi
			if [ "${use_modules}" = "1" ];then
				emerge --ignore-default-opts --oneshot --jobs @module-rebuild
			fi
		fi
		kernel-initramfs-dracut -k "${kver_full}"
		kernel-grub
		if [ "${clean_kernel_src}" = "1" ];then
			kernel-clean-src -c
		fi
	fi
fi
