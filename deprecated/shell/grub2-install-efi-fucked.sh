#!/usr/bin/env sh
#2.3.0
#2019-12-23

# Copyright (C) 2018,2019 Brandon Zorn <brandonzorn@cock.li>
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

mkconfig="0"
while getopts "hm" OPT;do
	case "$OPT" in
		m) mkconfig="1";;
		h)
			printf " -h\tPrint this help\n"
			printf " -m\tupdate grub.cfg\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

g=$(grub-install --target=x86_64-efi --efi-directory=/boot/efi)

. "$(dirname "$0")/colors.sh"
printf "\n${BYEL}Someone fucked up the boot loader again${NC}\n\n"

if [ "$(echo "${g}"|grep error)" ];then
	printf "${RED}==================${NC}\n"
	printf "${RED}= Error stopping =${NC}\n"
	printf "${RED}==================${NC}\n\n"
	printf "${g}\n\n"
	die
else
	printf "${g}\n\n"
	if [ "${mkconfig}" = "1" ] && [ -x "$(dirname "$0")/kernel-grub" ];then
		"$(dirname "$0")"/kernel-grub
	elif [ "${mkconfig}" = "1" ];then
		grub-mkconfig -o /boot/grub/grub.cfg
	fi
	[ -x /usr/sbin/efibootmgr ] && printf "\n${YEL}Check below is correct${NC}\n" && /usr/sbin/efibootmgr
fi
