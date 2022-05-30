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
# 5.7.1
# 2019-02-24


#TODO
#xargs
#size target
#acceptable size range
#rezizing when w > h

die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }

convert_main()
{
	if [ "${batch}" = "1" ];then
		batch="0"
		nest_dir="$(find . -mindepth 2 -path '*/*' -type d)"
		if [ -n "${nest_dir}" ];then printf "Nested directories detected\n\n%s\n\n" "${nest_dir}";fi
		if [ "${mimecheck}" = "1" ];then mime-correct -A;mimecheck="0";fi
		for d in *;do
			if [ -d "${d}" ];then
				cd "${d}" || die
				printf "Running in: %s\n" "${d}"
				convert_main "${1}"
				cd .. || die
			fi
		done
		exit
	fi
	if ! [ "${act}" = "get_size" ];then
		if [ "${mimecheck}" = "1" ];then mime-correct -I;fi
		mkdir -p "${O}"
		tmpdir="$(mktemp -p . -d)"
	fi
	for f in *;do
		if [ -n "$(file -b --mime-type -- ${f%%}|grep image)" ];then
			case "${1}" in
				convert)
					if ! [ -f "${f%%.*}.${newext}" ];then
						gm convert -quality ${qual} "${f%%.*}.${origext}" "${tmpdir}/${f%%.*}.${newext}"
						mv "${f}" "${O}"
					else
						if [ "${debug}" = "1" ];then
							printf "Skipping: ${f}\n"
						fi
					fi
					;;
				convert_auto)
					if [ "${newext}" = "jpg" ];then
						qual="100"
					else
						qual="9"
					fi
					if [ "${debug}" = "1" ];then iter="1";fi
					while true;do
						if [ "${debug}" = "1" ];then printf "iter %s\n" "${iter}";fi
						gm convert -quality ${qual} "${f%%}" "${tmpdir}/${f%.*}.${newext}"
						test_size "${f%%}" "${tmpdir}/${f%.*}.${newext}"
						if [ "${new_is_smaller}" = "1" ];then
							new_is_smaller="0"
							printf "final qual is %s for %s\n" "${qual}" "${f}"
							mv "${f}" "${O}"
							break
						fi
						#runs when above if fails, so decrease $qual and try again
						qual=$((qual - 1))
						if [ "${debug}" = "1" ];then iter="$((iter + 1))";fi
					done
					;;
				resize)
					gm convert "${f%%}" -resize "${size}"\> "${tmpdir}/${f%%}"
					mv "${f}" "${O}"
					;;
				get_size)
					gm identify -format "%wx%h" "${f%%}"
					;;
			esac
		fi
	done
	if ! [ "${1}" = "get_size" ];then
		if [ "$(ls -A ${tmpdir}|wc -l)" -gt "0" ];then
			mv ${tmpdir}/* . #do not quote
		fi
		rm -rf "${tmpdir}"

		if [ "${keep_orig}" = "0" ];then
			rm -rf "${O}"
		elif [ -d "${O}" ] && ! [ "$(ls -A ${O})" ];then
			rm -rf "${O}"
		fi
	fi
}

test_size()
{
	orig="${1}"
	new="${2}"

	if [ "${debug}" = "1" ];then
		printf "filesize new  : $(du ${new}|awk '{print $1}')\n"
		printf "filesize orig : $(du ${orig}|awk '{print $1}')\n"
	fi

	if [ "$(du "${orig}"|awk '{print $1}')" -ge "$(du "${new}"|awk '{print $1}')" ];then
		new_is_smaller="1"
	fi
}

get_mode()
{
	if ! [ "${qual}" = "0" ];then
		act="convert"
	else
		act="convert_auto"
	fi
}

O="orig"
batch="0"
debug="0"
mimecheck="1"
keep_orig="1"
new_is_smaller="0"

if [ -z "${1}" ];then "${0}" -h;exit;fi
while getopts "dP:p:J:j:H:W:S:hmsBbr" OPT;do
	case "$OPT" in
		j)
			origext="jpg"
			newext="png"
			qual="${OPTARG}"
			if [ "${qual}" -gt "9" ];then printf "exiting because of invalid range: %s\n" "${OPTARG}";exit;fi
			get_mode
			;;
		J)
			origext="jpg"
			newext="jpg"
			qual="${OPTARG}"
			if [ "${qual}" -gt "100" ];then printf "exiting because of invalid range: %s\n" "${OPTARG}";exit;fi
			get_mode
			;;
		p)
			origext="png"
			newext="jpg"
			qual="${OPTARG}"
			if [ "${qual}" -gt "100" ];then printf "exiting because of invalid range: %s\n" "${OPTARG}";exit;fi
			get_mode
			;;
		P)
			origext="png"
			newext="png"
			qual="${OPTARG}"
			if [ "${qual}" -gt "9" ];then printf "exiting because of invalid range: %s\n" "${OPTARG}";exit;fi
			get_mode
			;;
		W)
			case "${OPTARG}" in
				1) size="2400";;
				2) size="1600";;
				3) size="1280";;
				4) size="980";;
				5) size="780";;
				*) size="${OPTARG}";;
			esac
			act="resize"
			;;
		H)
			case "${OPTARG}" in
				1) size="x2400";;
				2) size="x1600";;
				3) size="x1280";;
				4) size="x980";;
				5) size="x780";;
				*) size="x${OPTARG}";;
			esac
			act="resize"
			;;
		S)
			case "${OPTARG}" in
				[1-9]) size="${OPTARG}0%";;
				*) size="${OPTARG}";;
			esac
			act="resize"
			;;
		B)
			keep_orig="1"
			batch="1"
			;;
		b)
			keep_orig="0"
			batch="1"
			;;
		r) keep_orig="0";;
		s) act="get_size";;
		m) mimecheck="0";;
		d) debug="1";;
		h)
			printf "GENERAL\n"
			printf " -d\textra printouts\n"
			printf " -m\tdisable mime check\n"
			printf " -r\tdo not keep orig\n"
			printf " -s\tget current image size in dir\n"
			printf "\nBATCH\n"
			printf " example, %s -B -P 0\n" "${0}"
			printf " -B\tbatch, must come before other args\n"
			printf " -b\tbatch, must come before other args, uses -r\n"
			printf "\nRESIZE Width, keeps aspect\n"
			printf " -W *\tuse value provided\n"
			printf " -W 1\t2400x\n"
			printf " -W 2\t1600x\n"
			printf " -W 3\t1280x\n"
			printf " -W 4\t980x\n"
			printf " -W 5\t780x\n"
			printf "\nRESIZE Hight, keeps aspect\n"
			printf " -H *\tuse value provided\n"
			printf " -H 1\tx2400\n"
			printf " -H 2\tx1600\n"
			printf " -H 3\tx1280\n"
			printf " -H 4\tx980\n"
			printf " -H 5\tx780\n"
			printf "\nRESIZE Percent\n"
			printf " Increments in steps of 10%%\n"
			printf " -S 9\t90%%\n"
			printf " ..\n"
			printf " -S 1\t10%%\n"
			printf " -S *\tany percent, must append '%%'\n"
			printf "\nCONVERT\n"
			printf "value of '0' sets auto mode\n"
			printf "quality ranges, higher is better quality, JPG: 1-100, PNG:1-9\n"
			printf " -J [1-100]\tjpg > jpg\n"
			printf " -j [1-9]  \tjpg > png\n"
			printf " -P [1-9]  \tpng > png\n"
			printf " -p [1-100]\tpng > jpg\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done
#shift $((OPTIND - 1))

case "${act}" in
	convert)
		convert_main convert
		;;
	convert_auto)
		convert_main convert_auto
		;;
	resize)
		convert_main resize
		;;
	get_size)
		convert_main get_size
		;;
esac

