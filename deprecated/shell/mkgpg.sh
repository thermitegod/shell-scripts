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
# 3.11.0
# 2019-09-25


#TODO
#diffrent keys for encrypting

compress()
{
	case "${comp_crypt}" in
		0)
			printf "Encrypting : %s\n" "${f%%}"
			nice -19 gpg --yes --batch -e -r "${user}" "${f%%}"
			if [ "${comp_rm}" = "1" ];then rm -r "${f%%}";fi
			;;
		1)
			printf "Decrypting : %s\n" "${f%%}"
			#printf "Output     : %s\n" "${f%%.*}"
			nice -19 gpg --output "${f%%.*}" --decrypt "${f%%}"
			;;
	esac
}

comp_crypt="0"
comp_files="0"
comp_rm="0"
user="brandon"

while getopts "dfsxlh" OPT;do
	case "$OPT" in
		l) gpg --list-secret-keys --keyid-format LONG;exit;;
		d) comp_crypt="1";;
		f) comp_files="1";;
		s) comp_rm="1";;
		x) comp_files="1";comp_rm="1";;
		h)
			printf " default will gpg files passed in \$1\n"
			printf " -d\tDecrypt\n"
			printf " -f\tgpg all files\n"
			printf " -h\tprint this help\n"
			printf " -l\tprint available keys\n"
			printf " -s\tgpg \$1, delete after gpg\n"
			printf " -x\tgpg all files, delete original after gpg\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done
shift $((OPTIND - 1))

if [ -n "${1}" ];then
	while true;do
		f="${1%%}"
		if [ -e "${f}" ];then
			compress
		else
			printf "\nInput is none existent : %s\n\n" "${1}"
		fi
		if [ -n "${2}" ];then shift;else break;fi
	done
elif [ "${comp_files}" = "1" ];then
	for f in *; do if [ -f "${f}" ];then compress;fi;done
else
	printf "Nothing to compress\n";exit
fi
