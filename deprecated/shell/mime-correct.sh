#!/usr/bin/env sh
#2.5.0
#2019-09-25

# Copyright (C) 2018,2019 Brandon Zorn <brandonzorn@cock.li>
#
# This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 3
#    as published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <https://www.gnu.org/licenses/>.

#ref
#collision -- same filename when corrected
#mismatch -- wrong file extension

mime_type_image()
{
	if [ -d "${f}" ];then return;fi
	total="$((total+1))"
	mimeext=$(file -b --mime-type -- "${f%%}"|awk '{print $NF}' FS=/)
	if [ "${mimeext##*-}" = "bmp" ];then mimeext="bmp";fi
	if ! [ "${mimeext}" = "jpeg" ] && ! [ "${mimeext}" = "png" ] && ! [ "${mimeext}" = "gif" ] && \
		! [ "${mimeext}" = "tiff" ] && ! [ "${mimeext}" = "bmp" ];then return;fi
	ext="${f##*.}"
	if [ "${mimeext}" = "jpeg" ] && [ "${ext}" = "jpg" ];then return;fi
	if [ "${mimeext}" = "jpeg" ];then mimeext="jpg";fi
	if ! [ "${mimeext}" = "${ext}" ];then
		if [ -f "${f%%.*}.${mimeext}" ] && [ -f "${f%%.*}.${ext}" ];then
			if [ "${V}" = "1" ];then
				if [ "$(openssl sha1 "${f%%.*}.${mimeext}"|awk '{print $2}')" = "$(openssl sha1 "${f%%.*}.${ext}"|awk '{print $2}')" ];then
					if [ "${sha_coll_rm}" = "1" ];then rm "${f%%}";return;fi
					printf "${YEL}File collision is same file${NC}: %s %s\n" "${f%%.*}.${mimeext}" "${f%%.*}.${ext}"
				else
					printf "${YEL}File collision with different files${NC}: %s %s\n" "${f%%.*}.${mimeext}" "${f%%.*}.${ext}"
				fi
			fi
			coll="$((coll+1))"
			return
		else
			if [ "${V}" = "1" ];then printf "${YEL}Mismatch${NC}: %s\n" "$(readlink -f "${f%%}")";fi
		fi
		if [ "${listonly}" = "1" ];then return;fi
		mv "${f%%}" "${f%%.*}.${mimeext}"
		fixed="$((fixed+1))"
	fi
}

. "$(dirname "$0")/colors.sh"

if [ -z "${1}" ];then "${0}" -h;exit;fi
while getopts "AILvhr" OPT;do
	case "$OPT" in
		A) mode="check_all";;
		I) mode="check";listonly="0";;
		L) mode="check";listonly="1";sha_coll_rm="0";;
		r) export sha_coll_rm="1";;
		v) export V="1";;
		h)
			printf "Correct incorrect file extensions based on mime type, supports: jpg,png,gif,tiff,bmp\n"
			printf " -A\trun in all sub-dirs of \$PWD\n"
			printf " -h\tprint this help\n"
			printf " -I\trun in single dir only\n"
			printf " -L\tlist only in \$PWD, no corrections\n"
			printf " -r\tif two files collide with the same sha1 hash, remove the file with the incorrect file extension\n"
			printf " -v\tverbose\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

case "${mode}" in
	check)
		total="0"
		coll="0"
		fixed="0"
		for f in *;do mime_type_image;done
		if ! [ "${fixed}" = "0" ];then fixed_out="\t${YEL}Corrected${NC}: ${fixed}";else fixed_out="";fi
		if ! [ "${coll}" = "0" ];then coll_out="\t${RED}Collision${NC}: ${coll}";else coll_out="";fi
		if [ "${V}" = "1" ];then pwd_out="\tin: ${PWD}";else pwd_out="";fi
		if ! [ "${total}" = "0" ];then printf "${GRE}Checked${NC}: ${total}${fixed_out}${coll_out}${pwd_out}\n";fi
		;;
	check_all)
		find "$(pwd)" -path '*/*' -type d \( ! -name . \)|while read -r dir;do cd "${dir}" && "${0}" -I;done
		;;
esac

