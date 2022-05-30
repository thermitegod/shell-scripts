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
# 2.9.0
# 2019-09-25


die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }

array="$(seq -w -s ' ' "$(ls -1A|wc -l)")"
mode="single"
V="1"

. "$(dirname "$0")/colors.sh"

while getopts "v:bh" OPT;do
	case "$OPT" in
		b) mode="batch";;
		v)
			case "${OPTARG}" in
				0) V="0";;
				1) V="1";;
				2|*) V="2";;
			esac;;
		h)
			printf " -b\tBatch mode\n"
			printf " -h\tPrint this help\n"
			printf " -v\tverbose level [0-2]\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

case "${mode}" in
	single)
		for f in $(ls -1A|sort -V);do
			if [ -f "${f%%}" ];then
				array1=$(echo "$array"|cut -d ' ' -f 1)
				newname="${array1}.${f##*.}"
				if ! [ -f "${newname}" ];then
					mv -- "${f%%}" "${newname}"
					if [ "${V}" -ge "2" ];then printf "${GRE}renamed${NC}: %s %s\n" "${f%%}" "${newname}";fi
				else
					if [ "$(openssl sha1 "${f%%}"|awk '{print $2}')" = "$(openssl sha1 "${newname}"|awk '{print $2}')" ];then
						if [ "${V}" -ge "1" ];then printf "${YEL}Same File not renaming${NC}: %s" "${f%%}";fi
					else
						if [ "${V}" -ge "1" ];then
							printf "${YEL}Diferent files with same filename would exist${NC}\n"
							printf "\nORIG:\t%s\nNEW:\t%s\n" "${f%%}" "${newname}"
						fi
					fi
				fi
				array=$(echo "${array}"|sed "s/[^ ]* //")
			fi
		done
		;;
	batch)
		find . -path '*/*' -type d \( ! -name . \)|while read -r dir;do cd "${dir}" || die && "${0}";done
		;;
esac
