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
# 2019-05-17


die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }

if [ "$(id -u)" -ne 0 ];then die "Requires root, exiting.";fi
finish(){ if [ -d "${tmpdir}" ];then rm --preserve-root -r "${tmpdir}";fi }
trap 'exit 1' INT HUP QUIT TERM USR1
trap finish EXIT
tmpdir=$(mktemp -d)

clean()
{
	mv .config "${tmpdir}"
	make distclean
	mv "${tmpdir}"/.config .
}

kdir="/usr/src/linux"
while getopts "rcCh" OPT;do
	case "$OPT" in
		r)
			for f in ${kdir}*;do
				rm -rf "${f}"
			done
			exit;;
		c)
			cd "${kdir}" || die
			clean
			exit;;
		C)
			for f in ${kdir}-*;do
				cd "${f}" || die
				clean
			done
			exit;;
		h)
			printf " -c\tclean only /usr/src/linux symlink\n"
			printf " -C\tclean /usr/src/linux-*\n"
			printf " -h\tprint this help\n"
			printf " -r\tremove all /usr/src/linux*\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done
