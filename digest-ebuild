#!/usr/bin/env sh
#2.7.0
#2019-09-24

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

while getopts "ah" OPT;do
	case "$OPT" in
		a)
			find "$PWD" -maxdepth 2 -mindepth 2 -type d -not -path "*/.git/*" | \
				while read -r dir;do cd "${dir}" || die && "${0}";done;exit;;
		h)
			printf " -a\trun for the entire repo\n"
			printf " -h\tprint this help\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

ebuild "$(ls -1A ./*.ebuild|tail -n1)" manifest
