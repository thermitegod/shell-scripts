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
# 5.4.0
# 2019-09-25


die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }
test_file_list(){ if [ -f "${f%%}.zip" ];then file_list="${file_list}${delim}${f%%}.zip";fi; }
compress()
{
	case "${comp_type}" in
		0)
			nice -19 zip -rv -9 --junk-paths "${f%%}.zip" "${f%%}" || die "Compression failed for: ${f%%}"
			test_file_list
			;;
		1)
			nice -19 zip -rv -9 "${f%%}.zip" "${f%%}" || die "Compression failed for: ${f%%}"
			test_file_list
			;;
		test)
			if [ "${f##*.}" = "zip" ];then
				case "${test_mk7z}" in
					0) nice -19 unzip -tq "${f%%}";;
					1) mk7z -T "${f%%}";;
				esac
				return
			fi
			;;
	esac

	if [ "$?" -eq 0 ] && ! [ "${comp_type}" = "test" ] && [ "${orig_rm}" = "1" ] && [ -f "${f%%}.zip" ];then
		if [ -n "$(${0} -t "${f%%}.zip"|grep FAILED)" ];then
			printf "Test FAILED for: %s.7z\nNot removing original: %s\n" "${f%%}" "${f%%}"
		else
			rm -r "${f%%}"
		fi
	fi
}

orig_rm="0"
comp_dir="0"
comp_files="0"

comp_type="0"
test_post="1"
test_mk7z="1"
file_list=""

delim=",ßßß,"

while getopts "TZFDPRtdfszh" OPT;do
	case "$OPT" in
		d) comp_dir="1";;
		D) comp_dir="1";comp_type="1";;
		f) comp_files="1";;
		F) comp_files="1";orig_rm="1";;
		P) test_post="0";;
		s) orig_rm="1";;
		R) orig_rm="1";test_post="0";;
		t) comp_type="test";;
		T) comp_type="test";test_mk7z="0";;
		z) comp_dir="1";orig_rm="1";;
		Z) comp_dir="1";orig_rm="1";comp_type="1";;
		h)
			printf " -d\tcompress all directories, junk path\n"
			printf " -D\tcompress all directories, dont junk path\n"
			printf " -f\tcompress all files\n"
			printf " -F\tcompress all files, delete original after compressed\n"
			printf " -h\tprint this help\n"
			printf " -P\tDisable post compression test\n"
			printf " -s\tcompress \$1, delete after compressed\n"
			printf " -R\tdelete after compressed, will test before deleting, disables post testing, works in all modes but test\n"
			printf " -t\tTest all files or files passed in \$1, using mk7z -t : prefered test method\n"
			printf " -T\tTest all files or files passed in \$1, using unzip -tq\n"
			printf " -z\tcompress all directories, delete original after compressed, junk path\n"
			printf " -Z\tcompress all directories, delete original after compressed, dont junk path\n"
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
elif [ "${comp_dir}" = "1" ] || [ "${comp_files}" = "1" ];then
	for f in *; do
		if [ "${comp_dir}" = "1" ] && [ -d "${f%%}" ];then compress;fi
		if [ "${comp_files}" = "1" ] && [ -f "${f%%}" ];then compress;fi
	done
else
	printf "Nothing to compress\n";exit
fi

if [ "${test_post}" = "1" ] && [ "${orig_rm}" = "0" ];then
	IFS="${delim}"
	for f in ${file_list}; do
		if [ -f "${f}" ];then
			comp_type="test"
			compress
		fi
	done
	unset IFS
fi
