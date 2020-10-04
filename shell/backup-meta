#!/usr/bin/env sh
#2.5.0
#2020-04-25

# Copyright (C) 2018,2019,2020 Brandon Zorn <brandonzorn@cock.li>
#
# This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 3
#    as published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <https://www.gnu.org/licenses/>.

die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }

finish(){ if [ -d "${tmpdir}" ];then rm --preserve-root -r "${tmpdir}";fi }
trap 'exit 1' INT HUP QUIT TERM USR1
trap finish EXIT
tmpdir=$(mktemp -d)

date=$(date "+%F-%H%M")
user="brandon"
group="${user}"
backup_dir="/mnt/data/backup"
comp="zstd"
V=""

dir_check(){ if ! [ -d "${target_dest}" ];then mkdir -p "${target_dest}";fi }
move_finish()
{
	chown "${user}:${group}" "${tmpdir}/${target_comp}"
	mv -iv "${tmpdir}/${target_comp}" "${target_dest}"
}

mode="${0##*/backup-}"
while getopts "12345hvxz" OPT;do
	case "$OPT" in
		1) mode="chromium";;
		2) mode="user-bin";;
		3) mode="user-config";;
		4) mode="user-local";;
		5) mode="etc";;
		v) V="v";;
		x) comp="xz";;
		z) comp="zstd";;
		h)
			printf "\nGENERAL\n"
			printf " -h\tprint this help\n"
			printf " -v\tverbose tar\n"
			printf " -x\tuse xz\n"
			printf " -z\tuse zstd\n"
			printf "\nCOMPRESS\n"
			printf " -1\tchromium\n"
			printf " -2\tuser-bin\n"
			printf " -3\tuser-config\n"
			printf " -4\tuser-local\n"
			printf " -5\tetc\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

case "${comp}" in
	zstd) C="zstd";A="-T0";E="zst";;
	xz) C="xz";A="-e9";E="xz";;
esac

case "${mode}" in
	chromium)
		target_source="${XDG_CONFIG_HOME}/chrome"
		target_dest="${backup_dir}/${user}/chromium-profiles/${date}"
		dir_check
		cd "${target_source}" || die
		for f in *chrom*;do
			target_comp="${date}-${user}-${f}.tar.${E}"
			tar \
				--exclude="${f}/Default/File System" \
				--xattrs --sparse -${V}cf - "${f}" -P | "$C" "$A" >| "${tmpdir}/${target_comp}"
			move_finish
		done
		;;
	user-bin)
		target_comp="${date}-${user}-bin.tar.${E}"
		target_source="${HOME}/.bin"
		target_dest="${backup_dir}/${user}/bin"
		dir_check
		mkdir "${tmpdir}"/bin
		cd "${tmpdir}" || die
		tar \
			--xattrs --sparse -${V}cf - "${target_source}" -P | "$C" "$A" >| "${tmpdir}/${target_comp}"
		move_finish
		;;
	user-config)
		target_comp="${user}-config-${date}.tar.${E}"
		target_source="${XDG_CONFIG_HOME}"
		target_dest="${backup_dir}/${user}/config"
		dir_check
		tar \
			--exclude="${target_source}/*chrom*" \
			--exclude="${target_source}/rtorrent/session/*" \
			--exclude="${target_source}/transmission/resume/*" \
			--exclude="${target_source}/transmission/torrents/*" \
			--exclude="${target_source}/kernel/src/*" \
			--exclude="${target_source}/kernel/distfiles/*" \
			--xattrs --sparse -${V}cf - "${target_source}" -P | "$C" "$A" >| "${tmpdir}/${target_comp}"
		;;
	user-local)
		target_comp="${user}-local-${date}.tar.${E}"
		target_source="${HOME}/.local"
		target_dest="${backup_dir}/${user}/local"
		dir_check
		tar \
			--exclude="${target_source}/share/Trash/*" \
			--xattrs --sparse -${V}cf - "${target_source}" -P | "$C" "$A" >| "${tmpdir}/${target_comp}"
		move_finish
		;;
	etc)
		target_comp="etc-${date}.tar.${E}"
		target_source="/etc"
		target_dest="${backup_dir}/etc"
		dir_check
		tar \
			--xattrs --sparse -${V}cf - "${target_source}" -P | "$C" "$A" >| "${tmpdir}/${target_comp}"
		move_finish
		;;
	meta) "${0}" -h;exit;;
esac
