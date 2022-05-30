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
# 4.12.0
# 2019-09-25


mimecheck="1"
V="0"
opt_level="5"
#5 is basically the same as 7, only 7 takes 80-100%~ longer for savings in the low double digit bytes, if at all.

mode="${0##*/}"
while getopts "vmjpghx" OPT;do
	case "$OPT" in
		v) V="1";;
		m) mimecheck="0";;
		j) mode="optimize-jpg";;
		p) mode="optimize-png";;
		g) mode="optimize-gif";;
		x) opt_level="7";;
		h)
			printf "MODE: Current is: %s\n" "${mode}"
			printf " -g\tforce mode=gif\n"
			printf " -j\tforce mode=jpg\n"
			printf " -p\tforce mode=png\n"
			printf "\nGENERAL\n"
			printf " -h\tprint this help\n"
			printf " -m\tdisanle mime check\n"
			printf " -x\tpng only, use -o7 instead of -o5\n"
			printf " -v\tPrint change in dir size\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

if [ "${mimecheck}" = "1" ];then mime-correct -A;fi
if [ ${V} = "1" ];then B="$(printf "Before : %s\n" "$(du|tail -n1)\t$(du -h|tail -n1)")";fi

case "${mode}" in
	optimize-jpg)
		find . -type f -iname '*.jp**' -print0 | \
			nice -19 xargs --max-args=1 --max-procs="$(nproc)" --null jpegoptim --strip-all --preserve --preserve-perms
		;;
	optimize-png)
		find . -type f -iname '*.png' -print0 | \
			nice -19 xargs --max-args=1 --max-procs="$(nproc)" --null optipng -o${opt_level} -strip all -preserve
		;;
	optimize-gif)
		find . -type f -iname '*.gif' -print0 | \
			nice -19 xargs --max-args=1 --max-procs="$(nproc)" --null gifsicle -bO3 -V
		;;
	optimize-all)
		#mimecheck will run during inital, dont run on subsequent
		"${0}" -m -g
		"${0}" -m -j
		"${0}" -m -p
		;;
esac

if [ ${V} = "1" ];then printf "%s\nAfter  : %s\n" "${B}" "$(du|tail -n1)\t$(du -h|tail -n1)";fi
