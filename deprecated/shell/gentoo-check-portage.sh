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
# 1.0.0
# 2019-09-05


#based on https://github.com/bunder2015/scripts/blob/master/gentoo/pclean.sh
#based on https://github.com/bunder2015/scripts/blob/master/gentoo/worldcheck.sh

port="/etc/portage"
world="/var/lib/portage/world"

portage_check(){
	if [ -f "${file}" ] && ! [ "$(echo ${file}|grep package.mask)" ];then
		printf "Running check on: %s\n" "${file}"
		while read -r i;do
			#if [ "${i}" = "\#*" ] || [ -z "${i}" ];then continue;fi #bash
			if [ "${i#\#}"x != "${i}x" ] || [ -z "${i}" ];then continue;fi #posix
			str="$(echo "${i}"|awk '{print $1}')"
			if ! [ "$(equery -q list "${str}" &>/dev/null)" ];then
				printf "%s\n" "${str}"
			fi
		done < "${file}"
	fi
	printf "\n\n"
	unset file
}

while getopts "f:ahpw" OPT;do
	case "$OPT" in
		f)
			file_ext="${OPTARG}"
			file="${port}/package.${file_ext}"
			portage_check
			;;
		a)
			pkg="$(ls -1A /etc/portage/package.*)"
			for file in ${pkg};do
				portage_check
			done
			;;
		p)
			pkg="$(ls -1A /etc/portage/package.*)"
			for f in ${pkg};do
				name="$(basename "${f}")"
				if ! [ "$(echo ${name}|grep package.mask)" ];then
					printf "%s\n" "${name}"
				fi
			done
			;;
		w)
			#printf "Check packages as USE=test will be detected as a dep even if not active\n\n"
			printf "Possible packages that can be removed from: %s\n" "${world}"
			while read -r p;do
				if equery depends "${p}" >> /dev/null;then
					printf "%s\n" "${p}"
				fi
			done < "${world}"
			;;
		h)
			printf "This script prints packages in %s/package.* files\nthat are not installed on the current system\n\n" "${port}"
			printf "GENERAL\n"
			printf " -h\tPrint this help\n"
			printf " -p\tPrint package.* files\n"
			printf "\nPACKAGE OPTS\n"
			printf " -a\tRun for all package.* files\n"
			printf " -f\tspecify package.* file, args are file ext (env,use,mask)\n"
			printf " -w\tcheck world file\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done
shift $((OPTIND - 1))

