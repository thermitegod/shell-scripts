#!/usr/bin/env sh
#3.4.0
#2019-05-17

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

verbose="1"
advall="0"
while getopts "aqh" OPT;do
	case "$OPT" in
		a) advall="1";;
		q) verbose="0";;
		h)
			printf " -a\trun for all zip files\n"
			printf " -h\tprint this help\n"
			printf " -q\tquiet\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done
shift $((OPTIND - 1))

if [ ${advall} = "1" ];then
	if [ ${verbose} = "1" ];then
		bf1=$(du|tail -n1)
		bf2=$(du -h|tail -n1)
	fi

	find . -type f -iname "*.zip" -print0 | nice -19 xargs --max-args=1 --max-procs="$(nproc)" --null advzip -z -4

	if [ ${verbose} = "1" ];then
		af1=$(du|tail -n1)
		af2=$(du -h|tail -n1)
		printf "Before : %s\t%s\n" "${bf1}" "${bf2}"
		printf "After  : %s\t%s\n" "${af1}" "${af2}"
	fi
else
	if [ -z "$1" ];then
		printf "Nothing to compress\n"
		exit
	fi
	nice -19 advzip -z -4 "${1}"
fi
