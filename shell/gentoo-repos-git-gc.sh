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
# 1.1.0
# 2019-01-13


die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }

if [ "$(id -u)" -ne 0 ];then die "Requires root, exiting.";fi

while getopts "Llrdh" OPT;do
	case "$OPT" in
		r)
			port="$(grep location /etc/portage/repos.conf/gentoo.conf|awk '{print $3}')"
			cd "${port}" || die
			printf "Running in: %s\n" "${port}"
			git gc --aggressive
			;;
		l)
			port="$(grep location /etc/portage/repos.conf/local.conf|awk '{print $3}')"
			cd "${port}" || die
			printf "Running in: %s\n" "${port}"
			git gc --aggressive
			;;
		d)
			dist="$(grep DISTDIR= /etc/portage/make.conf|sed 's/DISTDIR=//g;s/"//g')"
			for d in ${dist}/git3-src/*;do
				printf "Running in: %s\n" "${d}"
				cd "${d}" || die
				git gc --aggressive
				printf "\n\n"
			done
			;;
		L)
			lay="$(grep storage /etc/layman/layman.cfg|head -n1|awk '{print $3}')"
			for d in ${lay}/*;do
				if [ -d "${d}/.git" ];then #check if git, some can be rsync
					printf "Running in: %s\n" "${d}"
					cd "${d}" || die
					git gc --aggressive
					printf "\n\n"
				fi
			done
			;;
		h)
			printf "GENERAL\n"
			printf " -h\tPrint this help\n"
			printf "\nREPOS\n"
			printf " -d\trun for all git repos in \$DISTDIR/git3-src\n"
			printf " -l\trun in local repo\n"
			printf " -L\trun for all git repos in layman\n"
			printf " -r\trun in gentoo repo\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

