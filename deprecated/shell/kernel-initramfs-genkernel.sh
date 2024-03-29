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
# 2.3.0
# 2019-05-17


die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }

if [ "$(id -u)" -ne 0 ];then die "Requires root, exiting.";fi

if ! [ -f "/usr/src/linux/usr/gen_init_cpio" ];then die "Make sure the kernel is build first";fi

logfile="/dev/null"
comp="lz4"
loglevel="1"
extra_flags=""

while getopts "vlxhde" OPT;do
	case "$OPT" in
		e)
			extra_flags="${extra_flags} --lvm --luks --e2fsprogs"
			;;
		d)
			extra_flags="${extra_flags} --debug-cleanup"
			loglevel="5"
			logfile="/tmp/genkernel-initgen.log"
			;;
		v) logfile="/tmp/genkernel-initgen.log";;
		l) comp="lz4";;
		x) comp="xz";export XZ_OPT="-9e";;
		h)
			printf "GENERAL\n"
			printf " -d\textra verbose\n"
			printf " -e\tlvm encryption support\n"
			printf " -h\tprint this help\n"
			printf " -v\tlog to /tmp/genkernel-initgen.log\n"
			printf "\nCOMPRESSION\n"
			printf " -l\tcompress initramfs using : lz4 [default]\n"
			printf " -x\tcompress initramfs using : xz \n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

genkernel initramfs \
	--logfile=${logfile} \
	--makeopts=-j$(($(nproc)+1)) \
	--loglevel=${loglevel} \
	--no-ramdisk-modules \
	--busybox \
	--no-keymap \
	--postclear \
	--disklabel \
	--compress-initramfs \
	--compress-initramfs-type=${comp} \
	--no-lvm \
	--no-mdadm \
	--no-nfs \
	--no-dmraid \
	--no-btrfs \
	--no-multipath \
	--no-iscsi \
	--no-hyperv \
	--no-ssh \
	--no-luks \
	--no-gpg \
	--no-mountboot \
	--no-unionfs \
	--no-netboot \
	--no-e2fsprogs \
	--no-dmraid \
	--zfs \
	--microcode \
	--firmware \
	--firmware-dir=/lib/firmware ${extra_flags}
