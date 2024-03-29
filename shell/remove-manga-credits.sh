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
# 5.5.0
# 2019-09-25


zzz="1"
act="ls"

d="/mnt/data/hentai-processing/credits"

find_credits()
{
	case "${act}" in
		ls)
			j=$(find . -iname "${1}" -exec ls -1A -- "{}" \;)
			if [ -n "${j}" ];then printf "\n\n\nFound 'POSSIBLE' credit files\n\n%s\n" "${j}";fi
			;;
		mv)
			#overwrites same filenames
			find . -type f -iname "${1}" -exec mv -v -- "{}" "${d}" \;
			;;
		trash)
			find . -type f -iname "${1}" -exec trash-put -- "{}" "${d}" \;
			;;
	esac
}

if [ -z "${1}" ];then "${0}" -h;exit;fi
while getopts "Tmltzh" OPT;do
	case "$OPT" in
		m) act="mv";;
		l) act="ls";;
		t) act="trash";;
		T) d="/tmp/test/credits";;
		z) zzz="0";;
		h)
			printf "GENERAL\n"
			printf " -h\tprint this help\n"
			printf " -T\tUse test dir '/tmp/test'\n"
			printf " -z\tDisable 'zzz' matching\n"
			printf "\nACTIONS\n"
			printf " -l\tList found\n"
			printf " -m\Move found\n"
			printf " -t\Trash found\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

find_credits *credit*.j*pg
find_credits *credit*.png
if [ "${zzz}" = "1" ] || [ "${act}" = "ls" ];then
	find_credits *zzz*.j*pg
	find_credits *zzz*.png
fi
