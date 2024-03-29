#!/usr/bin/env bash

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
# 2.5.0
# 2019-09-25


die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }

mode="single"
while getopts "bh" OPT;do
	case "$OPT" in
		b) mode="batch";;
		h)
			printf " -b\tBatch mode\n"
			printf " -h\tPrint this help\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

case "${mode}" in
	single)
		shopt -s nullglob
		shopt -s extglob
		for f in *.cue;do
			cuebreakpoints "${f%.*}".cue | shnsplit -t "%n-%t" -o flac "${f%.*}".flac
			#mv "${f%.*}".flac ../
		done
		;;
	batch)
		find . -maxdepth 1 -type d \( ! -name . \)|while read -r dir;do cd "${dir}" || die && "${0}";done
		;;
esac
