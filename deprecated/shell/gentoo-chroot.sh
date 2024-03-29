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
# 5.9.0
# 2019-09-25


die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }
if [ "$(id -u)" -ne 0 ];then die "Requires root, exiting.";fi
ch_1(){ ch="/mnt/gentoo"; }
ch_2(){ ch="/mnt/gentoo-gcc"; }
#ch_3(){ ch="/mnt/" ; }

mount_sys()
{
	if ! [ -d "${ch}/proc" ];then die "Missing directory ${ch}/proc";fi
	if ! [ -d "${ch}/sys" ];then die "Missing directory ${ch}/sys";fi
	if ! [ -d "${ch}/dev" ];then die "Missing directory ${ch}/dev";fi

	mount -t proc proc "${ch}/proc"
	mount --rbind /sys "${ch}/sys"
	mount --rbind /dev "${ch}/dev"
}

mount_in_chroot()
{
	chroot "${ch}" mount /tmp
	chroot "${ch}" mount /run
	chroot "${ch}" mount /usr/src
	#chroot "${ch}" mount /var/cache
}

mount_bind()
{
	repos="/var/db/repos"
	pkg=$(grep PKGDIR= /etc/portage/make.conf|sed 's/PKGDIR=//g;s/"//g')
	dist=$(grep DISTDIR= /etc/portage/make.conf|sed 's/DISTDIR=//g;s/"//g')

	if ! [ -d "${ch}/${repos}" ];then mkdir -p "${ch}/${repos}";fi
	if ! [ -d "${ch}/${pkg}" ];then mkdir -p "${ch}/${pkg}";fi
	if ! [ -d "${ch}/${dist}" ];then mkdir -p "${ch}/${dist}";fi

	mount --rbind "${pkg}" "${ch}/${pkg}"
	mount --rbind "${repos}" "${ch}/${repos}"
	mount --rbind "${dist}" "${ch}/${dist}"
}

shell_check()
{
	if [ -f "${ch}/bin/zsh" ];then S="zsh"
	elif [ -f "${ch}/bin/bash" ];then S="bash"
	else die "no shells in chroot"
	fi
}

setup="init"
mountbind="1"

while getopts "Abh" OPT;do
	case "$OPT" in
		A) setup="bind";;
		b) mountbind="0";;
		h)
			printf " -A\tOnly mount binds\n"
			printf " -b\tDont mount binds\n"
			printf " -h\tprint this help\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

printf "Gentoo chroot location\n"
ch_1;printf "1: ${ch}\n"
ch_2;printf "2: ${ch}\n"
#ch_3;printf "3: ${ch}\n"
unset ch
read ch_loc

case "${ch_loc}" in
	1) ch_1;;
	2) ch_2;;
	*) die "INVALID"
esac

case "${setup}" in
	init)
		shell_check
		mount_sys
		mount_in_chroot
		if [ "${mountbind}" = "1" ];then mount_bind;fi
		chroot "${ch}" /bin/${S}
		;;
	bind)
		mount_bind
		;;
esac
