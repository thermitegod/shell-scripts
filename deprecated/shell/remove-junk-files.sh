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
# 4.11.0
# 2019-09-25


act="ls"

url="0"
txt="0"
json="0"
other="0"

find_junk()
{
	case "${act}" in
		ls)
			j="$(find . -iname "${1}" -exec ls -1A -- "{}" \;)"
			if [ -n "${j}" ];then printf "\n\n\nFound %s files\n\n%s\n" "${1}" "${j}";fi
			;;
		rm)
			find . -type f -iname "${1}" -exec trash-put -- "{}" \;
			;;
	esac
}

if [ -z "${1}" ];then "${0}" -h;exit;fi
while getopts "ARrltjuoh" OPT;do
	case "$OPT" in
		r) act="rm";;
		l) act="ls";;
		R) act="rm";txt="1";json="1";url="1";other="1";;
		A) txt="1";json="1";url="1";other="1";;
		t) txt="1";;
		j) json="1";;
		u) url="1";;
		o) other="1";;
		h)
			printf "General\n"
			printf " -h\tprint this help\n"
			printf " -l\tprint all files matching search patterns\n"
			printf " -r\tRemove enabled pattern files\n"
			printf " -R\tRemove all pattern files\n"
			printf "Patterns\n"
			printf " -A\tEnable ALL patterns\n"
			printf " -j\tEnable json\n"
			printf " -o\tEnable md5/nfo/svf/bridgesort/padding_file\n"
			printf " -t\tEnable txt\n"
			printf " -u\tEnable url/mht/htm/html\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

find_junk desktop.ini
find_junk Thumbs.db
find_junk .DS_Store
find_junk __MACOSX

if [ ${other} = "1" ] || [ "${act}" = "ls" ];then
	find_junk *.md5
	find_junk *.nfo
	find_junk *.sfv
	find_junk .BridgeSort
	find_junk _____padding_file*
fi

if [ ${url} = "1" ] || [ "${act}" = "ls" ];then
	find_junk *.url
	find_junk *.mht
	find_junk *.htm
	find_junk *.html
fi

if [ ${txt} = "1" ] || [ "${act}" = "ls" ];then find_junk *.txt;fi
if [ ${json} = "1" ] || [ "${act}" = "ls" ];then find_junk *.json;fi
