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
# 5.7.0
# 2019-09-25


#TODO
#use mimetype for sorting

mode="${0##*/}"
case "${mode}" in
	count-image)
		type="PNG JPG JPEG JPE GIF BMP ICO WEBM MP4 MKV"
		;;
	count-archive)
		type="ZIP 7Z RAR CBR CBZ CB7 TAR BZ2 GZ LZ4 LZO XZ ZST"
		mode="archive"
		;;
esac

if [ -n "${1}" ];then D="${1}";else D=".";fi

count="0"
list="0"
while getopts "lh" OPT;do
	case "$OPT" in
		l) list="1";;
		h)
			printf "MODE  : %s\n" "${mode}"
			printf "TYPES : %s\n" "${type}"
			printf " -h\tprint this help\n"
			printf " -l\tlist found archives, restricted to mode=archive\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done
shift $((OPTIND - 1))

for f in ${type};do
	#cnt=$(find ${D} -type f -iname "*.${f}"|wc -l)
	cnt=$(find . -type f -iname "*.${f}"|wc -l)
	if ! [ "${cnt}" = "0" ];then printf "%s\t: %s\n" "${f}" "${cnt}";fi
	count=$((cnt+count))
done

if ! [ "${count}" = "0" ];then printf "Total\t: %s\n" "${count}";fi

if [ "${list}" = "1" ] && [ "${mode}" = "archive" ];then
	read -r -p "List found [yn]? " confirm
	if echo "${confirm}" | grep -iq "^y" ;then
		for f in ${type}; do
			printf "Listing all of: %s\n" "${f}"
			find . -iname "*.${f}"
		done
	fi
fi
