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
# 4.7.0
# 2020-03-28


die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }
finish(){ if [ -d "${tmpdir}" ];then rm --preserve-root -r "${tmpdir}";fi }
trap 'exit 1' INT HUP QUIT TERM USR1
trap finish EXIT
tmpdir="$(mktemp -d)"
chmod 755 "${tmpdir}"

while getopts "Bih" OPT;do
	case "$OPT" in
		B) find . -maxdepth 1 -type d \( ! -name . \)|while read -r dir;do cd "${dir}" || die && "${0}";done;exit;;
		i) inc_iso="1";;
		h)
			printf " -B\tBatch mode\n"
			printf " -h\tPrint this help\n"
			printf " -i\tInclude iso files\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

printf "Tmpdir: %s\n" "${tmpdir}"
for f in *;do
	mimetype=$(file -b --mime-type "${f%%}")
	ext="${f##*.}"
	case "${ext}" in
		mkv)
			printf "Skipping mkv file: %s" "${f}"
			;;
		iso|ISO)
			if [ "${inc_iso}" = "1" ];then
				find . -iname '*.iso' -exec 7z x -- "{}" \;
				cd ./VIDEO_TS || die "VIDEO_TS does not exist, check that this is a video iso"
				rm -- *BUP *IFO
				find . -maxdepth 1 -type f -size +0k -size -5M -exec rm -- "{}" \;
				for v in *;do
					#will prefix all *.VOB files w/ iso name
					ffmpeg -hide_banner -i "${v}" -c:a copy -c:v copy -c:s copy "${tmpdir}/${f%%.*}-${v%%}.mkv"
						#|| die "ERROR: conversion failed for ${v%%}"
				done
				cd .. || die
				mv -i "${tmpdir}/*.mkv" . || die "ERROR: cannot move ${tmpdir}/\*.mkv to ${PWD}"
				rm -rf -- ./AUDIO_TS ./VIDEO_TS
			fi
			;;
		*)
			if [ "${mimetype%%/*}" = "video" ];then
				O="${PWD%%}/original"
				if ! [ -d "${O}" ];then mkdir -p "${O}";fi
				ffmpeg -hide_banner -i "${f}" -c:a copy -c:v copy -c:s copy "${tmpdir}/${f%%.*}.mkv" \
					|| die "ERROR: conversion failed for ${f%%}"
				mv -i "${tmpdir}/${f%%.*}.mkv" "${PWD}" || die "ERROR: cannot move ${tmpdir}/${f%%.*}.mkv to ${PWD}"
				mv -i "${f}" "${O}" || die "ERROR: cannot move ${PWD}/${f%%} to ${O}"
				if [ -d "${O}" ] && ! [ "$(ls -A "${O}")" ];then rm -rf "${O}";fi
			fi
			;;
	esac
done

