#!/usr/bin/env sh
#1.1.0
#2020-04-25

# Copyright (C) 2020 Brandon Zorn <brandonzorn@cock.li>
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

while getopts "S:s:h" OPT;do
	case "$OPT" in
		s)
			repo="${OPTARG}"
			cd "${repo}" || die
			printf "Running in: %s\n" "${repo}"
			git -c gc.reflogExpire=0 \
				-c gc.reflogExpireUnreachable=0 \
				-c gc.rerereresolved=0 \
				-c gc.rerereunresolved=0 \
				-c gc.pruneExpire=now gc
			git gc --aggressive
			;;
		S)
			repo="$(readlink -e ${OPTARG})"
			for d in ${repo}/*;do
				if [ -d "${d}" ];then
					cd "${d}" || die
					printf "Running in: %s\n" "${d}"
					git -c gc.reflogExpire=0 \
						-c gc.reflogExpireUnreachable=0 \
						-c gc.rerereresolved=0 \
						-c gc.rerereunresolved=0 \
						-c gc.pruneExpire=now gc
					git gc --aggressive
					printf "\n\n"
				fi
			done
			;;
		h)
			printf "GENERAL\n"
			printf " -h\tPrint this help\n"
			printf "\nREPOS\n"
			printf " -s\trun in single repo\n"
			printf " -S\trun in all repos in directory\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

