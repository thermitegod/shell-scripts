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
# 4.4.1
# 2019-08-01


die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }

while getopts "Bh" OPT;do
	case "$OPT" in
		B) find . -maxdepth 1 -type d \( ! -name . \)|while read -r dir;do cd "${dir}" || die && "${0}";done;exit;;
		h)
			printf " -B\tEnable batch mode\n"
			printf " -h\tPrint this help\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

O="${PWD}/original"
if ! [ -d "${O}" ];then mkdir "${O}";fi

for f in *;do
	mimetype=$(file -b --mime-type "${f%%}")
	ext="${f##*.}"
	if [ -f "${f%%}" ] && ! [ "${ext}" = "opus" ] && [ "${mimetype%%/*}" = "audio" ] || [ "${mimetype%%/*}" = "video" ];then
		ffmpeg -hide_banner -i "${f}" -acodec libopus -b:a 128k -vbr on \
			-compression_level 10 -map_metadata 0 -id3v2_version 3 "${f%.*}".opus
		mv -iv "${f}" "${O}"
	fi
done

if [ -d "${O}" ] && ! [ "$(ls -A "${O}")" ];then rm -rf "${O}";fi
