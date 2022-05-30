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
# 3.4.0
# 2019-12-14


die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }

if [ "$(id -u)" -ne 0 ];then die "Requires root, exiting.";fi

for f in /dev/disk/by-id/ata-*;do
	if ! [ "$(echo "${f}"|grep part)" ];then
		len="$(echo "${f##*/}"|wc -m)"
		temp="$(smartctl -a "${f}"|grep Celsius|awk '{print $10}')"
		case "${len}" in
			3[2-9]|40)
				tab="\t\t\t"
				;;
			4[0-8])
				tab="\t\t"
				;;
			[1-3][0-1])
				printf "below lower format\nlen: %s\ndevice: %s\n" "${len}" "${f}"
				;;
			[4-9][7-9])
				printf "above upper format\nlen: %s\ndevice: %s\n" "${len}" "${f}"
				;;
		esac
		if [ -z "${temp}" ];then
			temp="UNKNOWN"
		else
			temp="${temp}°c"
		fi
		printf "${f}${tab}${temp}\n"
	fi
done
