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
# 3.3.0
# 2019-09-25


#TODO
#custom range

file_sort()
{
	find . -maxdepth 1 -type f -size +"${lower}" -size -"${upper}" -exec mkdir -p "${upper}" \; -quit
	find . -maxdepth 1 -type f -size +"${lower}" -size -"${upper}" -exec mv -i -- "{}" "${upper}" \;
}

if [ -z "${1}" ];then "${0}" -h;exit;fi

while getopts "m:g:alh" OPT;do
	case "$OPT" in
		a) mode="all";;
		m)
			case "${OPTARG}" in
				10) mode="less10M";;
				100) mode="less100M";;
				150) mode="less150M";;
				200) mode="less200M";;
				500) mode="less500M";;
			esac
			;;
		g)
			case "${OPTARG}" in
				1) mode="less1G";;
				10) mode="less10G";;
				100) mode="less100G";;
			esac
			;;
		l) count-size;exit;;
		h)
			printf "Sort files by size \n"
			printf " -a\tsort everything\n"
			printf " -h\tprint this help\n"
			printf " -l\tprint number of each file size\n"
			printf "\nSORT\n"
			printf " -m <level>\n"
			printf "\t10 : Sort less than 10M\n"
			printf "\t100: Sort less than 100M\n"
			printf "\t150: Sort less than 150M\n"
			printf "\t200: Sort less than 200M\n"
			printf "\t500: Sort less than 500M\n"
			printf " -g <level>\n"
			printf "\t1  : Sort less than 1G\n"
			printf "\t10 : Sort less than 10G\n"
			printf "\t100: Sort less than 100G\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

case "${mode}" in
	less10M)
		lower="0k"
		upper="10M"
		file_sort
		;;
	less100M)
		lower="10M"
		upper="100M"
		file_sort
		;;
	less150M)
		lower="100M"
		upper="150M"
		file_sort
		;;
	less200M)
		lower="150M"
		upper="200M"
		file_sort
		;;
	less500M)
		lower="200M"
		upper="500M"
		file_sort
		;;
	less1G)
		lower="500M"
		upper="1G"
		file_sort
		;;
	less10G)
		lower="1G"
		upper="10G"
		file_sort
		;;
	less100G)
		lower="10G"
		upper="100G"
		file_sort
		;;
	all)
		"${0}" -m 10
		"${0}" -m 100
		"${0}" -m 150
		"${0}" -m 200
		"${0}" -m 500
		"${0}" -g 1
		"${0}" -g 10
		"${0}" -g 100
		;;
esac
