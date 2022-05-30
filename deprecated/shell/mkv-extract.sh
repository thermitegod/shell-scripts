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
# 2.6.0
# 2019-09-25


#TODO
#fix sub extract

mode="z"

if [ -z "${1}" ];then "${0}" -h;exit;fi
while getopts "asvh" OPT;do
	case "$OPT" in
		a) mode="aud";;
		s) mode="sub";;
		v) mode="vid";;
		h)
			printf " -a\tExtract audio track\n"
			printf " -h\tprint this help\n"
			printf " -s\tExtract sub track\n"
			printf " -v\tExtract video track\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

case "${mode}" in
	aud)
		find . -type f -name '*.mkv' | while read -r filename; do
			mkvmerge -i "${filename}" | grep "audio" | while read -r subline; do
				tracknumber="$(echo "${subline}" | grep -E -o "[0-9]{1,2}" | head -1)"
				subtitlename="${filename%.*}"
				mkvextract tracks "${filename}" "${tracknumber}:${subtitlename}.flac" > /dev/null 2>&1
				printf "Done extracting flac from %s\n" "${filename}"
			done
		done
		;;
	sub)
		printf "Sub extract will break if more than one track exists\n"
		find . -type f -name '*.mkv' | while read -r filename; do
			mkvmerge -i "${filename}" | grep "subtitles" | while read -r subline; do
				tracknumber="$(echo "${subline}" | grep -E -o "[0-9]{1,2}" | head -1)"
				subtitlename="${filename%.*}"
				mkvextract tracks "${filename}" "${tracknumber}:${subtitlename}.ssa" > /dev/null 2>&1
				#mv "${subtitlename}.ssa" "${PWD}"/ssa
				printf "Done extracting ssa from %s\n" "${filename}"
			done
		done
		;;
	vid)
		find "$DIR" -type f -name '*.mkv' | while read -r filename; do
			mkvmerge -i "${filename}" | grep 'video' | while read -r subline; do
				tracknumber="$(echo "${subline}" | grep -E -o "[0-9]{1,2}" | head -1)"
				subtitlename="${filename%.*}"
				mkvextract tracks "${filename}" "${tracknumber}:${subtitlename}.mkv" > /dev/null 2>&1
				printf "Done extracting flac from %s\n" "${filename}"
			done
		done
		;;
	*) printf "something is wrong\n";exit;;
esac
