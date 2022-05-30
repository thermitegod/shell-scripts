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
# 1.8.0
# 2019-09-25


die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }

main(){ equery b $(ldd "${elf}"|awk '{print $1}'|awk '$1=$1' ORS=' '); }

mode="list"
while getopts "lneh" OPT;do
	case "$OPT" in
		l) mode="list_sort";;
		n) mode="list_nover";;
		e) mode="list_emerge";;
		h)
			printf "No flag will be standard 'equery b' output\n"
			printf " -e\tPrint emergable list\n"
			printf " -h\tprint this help\n"
			printf " -l\tPrint sorted with versions\n"
			printf " -n\tPrint sorted no version list, package.*\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done
shift $((OPTIND - 1))

if [ -n "${1}" ];then
	elf="${1}"
else
	read -r -p "Enter ELF path: " elf
fi

if ! [ -f "${elf}" ];then
	die "Entered file does not exist"
fi

fileinfo="$(file "${elf}")"
if [ -z "$(echo "${fileinfo}"|grep ELF)" ];then
	die "Entered file is not marked as ELF"
elif [ -n "$(echo "${fileinfo}"|grep statically)" ];then
	die "Entered ELF file statically linked"
fi

case "${mode}" in
	list)
		main
		;;
	list_sort)
		main|awk '{print $1}'|sort -u
		;;
	list_nover)
		main|awk '{print $1}'|sort -u|sed 's/-r[0-9]//;s/-[^-]*$//'
		;;
	list_emerge)
		main|awk '{print $1}'|sort -u|sed 's/-r[0-9]//;s/-[^-]*$//'|awk '$1=$1' ORS=' '
		echo
		;;
esac
