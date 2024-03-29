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
# 2.3.0
# 2019-09-25


if [ -z "${1}" ];then "${0}" -h;exit;fi
while getopts "adfxh" OPT;do
	case "$OPT" in
		a) mode="sane";;
		d) mode="dir";;
		f) mode="file";;
		x) mode="ex";;
		h)
			printf "Will run in : %s\n" "$PWD"
			printf " -a\t-d and -f\n"
			printf " -d\tset 755 drwxr-xr-x | directories\n"
			printf " -f\tset 644 -rw-r--r-- | files\n"
			printf " -h\tprint this help\n"
			printf " -x\tset 755 -rwxr-x-rx | files execute\n"
			printf "\nCodes\n"
			printf "0\t---\n"
			printf "1\t--x\n"
			printf "2\t-w-\n"
			printf "3\t-wx\n"
			printf "4\tr--\n"
			printf "5\tr-x\n"
			printf "6\trw-\n"
			printf "7\trwx\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

alias chmod="chmod -v --preserve-root"
case "${mode}" in
	sane)
		nice -19 find . -type d -exec chmod 755 -- "{}" \;
		nice -19 find . -type f -exec chmod 644 -- "{}" \;
		;;
	dir)
		nice -19 find . -type d -exec chmod 755 -- "{}" \;
		;;
	file)
		nice -19 find . -type f -exec chmod 644 -- "{}" \;
		;;
	ex)
		nice -19 find . -type f -exec chmod 755 -- "{}" \;
		;;
esac
