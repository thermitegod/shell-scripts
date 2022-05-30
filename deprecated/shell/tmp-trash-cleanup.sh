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
# 2.1.0
# 2018-09-02


#auto clean the /tmp trash dir since it is on a tmpfs
#other trash locations can be delt w/ manually

set -euf

T="/tmp/.Trash-1000"

while getopts "hsr" OPT;do
	case "$OPT" in
		r)
			if [ -d "${T:=/tmp/.Trash-1000}" ];then
				rm -rf "${T}"
			fi
			exit;;
		s)
			if [ -d "${T:=/tmp/.Trash-1000}" ];then
				size="$(du -h "${T}"|tail -n1|awk '{print $1}')"
				printf "Trash size is: %s\n" "${size}"
			else
				printf "There is no trash dir\n"
			fi
			exit;;
		h)
			printf "TRASH: Trash dir is: %s\n" "${T}"
			printf " -s\tPrint size of trash dir\n"
			printf " -r\tRemove trash dir\n"
			printf "\nGENERAL\n"
			printf " -h\tPrint this help\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

