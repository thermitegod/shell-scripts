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
# 1.18.1
# 2020-09-18


mode="manga"
archivetype="z"

optimize="1"
match_zzz="0"
show_time="1"
comp_test="1"
mime_check="1"
comp_advzip="1"
remove_junk="1"
numerical_rename="0"
detect_nested_dirs="1"

while getopts "ADRMTOtrzmh" OPT;do
	case "$OPT" in
		A) comp_advzip="0";;
		D) detect_nested_dirs="0";;
		R) remove_junk="0";;
		M) mime_check="0";;
		t) show_time="0";;
		T) comp_test="0";;
		O) optimize="0";;
		r) numerical_rename="1";;
		z) match_zzz="1";;
		m) mode="hentai";;
		h)
			printf "General\n"
			printf " -h\tPrint this help\n"
			printf "Enable\n"
			printf " -m\tEnable hentai mode\n"
			printf " -r\tEnable numerical renaming\n"
			printf "Disable\n"
			printf " -A\tDisable mkadvzip\n"
			printf " -D\tDisable nested directory detection\n"
			printf " -M\tDisable mime checker\n"
			printf " -O\tDisable image optimizer\n"
			printf " -R\tDisable junk file removal\n"
			printf " -T\tDisable compressed file test\n"
			printf " -t\tDisable time total\n"
			printf " -z\tDisable zzz matching in credits\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

if [ "${detect_nested_dirs}" = "1" ];then
	nest_dir=$(find . -mindepth 2 -path '*/*' -type d)
	if [ -n "${nest_dir}" ];then
		printf "Nested directories detected\n\n%s\n\n" "${nest_dir}"
	fi
fi

if [ "${remove_junk}" = "1" ];then
	remove-junk-files -l
	remove-junk-files -Ar
fi

g=$(remove-manga-credits -l)
if [ -n "${g}" ];then
	printf "%s\n\n" "${g}"
	if [ "${mode}" = "hentai" ];then
		read -p "Enter to remove found credits " z;unset z
		if [ "${match_zzz}" = "1" ];then
			remove-manga-credits -mz
		else
			remove-manga-credits -m
		fi
	else
		printf "Printing found, will NOT remove, use -m to remove\n"
	fi
fi
unset g

if [ "${numerical_rename}" = "1" ];then
	rename-numerical-batch
fi

if [ "${mime_check}" = "1" ];then
	mime-correct -A
	printf "\n"
fi

printf "\n\nMode is : %s\n\n" "${mode}"
count-archive
count-image
printf "Size\t: %s\n" "$(du -h|tail -n1|awk '{print $1}')"

printf "Choose archive type [DEFAULT:1]\n"
printf "1: zip destructive\n"
printf "2: zip destructive nojunkpath\n"
printf "3: 7z dir destructive\n"
read -r archivetype

if [ "${show_time}" = "1" ];then
	datestart=$(date)
fi

if [ "${optimize}" = "1" ];then
	optimize-all -Mv
fi

case "${archivetype}" in
	1) mkzip -dzP;;
	2) mkzip -dZjP;;
	3) mk7z -dzP;;
	*) mkzip -dzP;;
esac

if [ "${comp_advzip}" = "1" ] && ! [ "${archivetype}" = "3" ];then
	mkadvzip
fi

if [ "${comp_test}" = "1" ];then
	mk7z -t ./*
fi

if [ "${show_time}" = "1" ];then
	printf "Started\t\t: %s\n" "${datestart}"
	printf "Finished\t: %s\n" "$(date)"
fi
