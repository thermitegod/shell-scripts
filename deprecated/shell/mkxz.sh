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
# 6.4.0
# 2019-09-25


die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }

compress()
{
	if [ -d "${f%%}" ] && ! [ "${comp_type}" = "status" ];then comp_type="dir";fi
	case "${comp_type}" in
		status)
			tar --xattrs -${V}Scf - "${f%%}" -P | \
				pv -s "$(du -sb "${f%%}" | awk '{print $1}')" | \
				$C >| "${f%%}.tar.${E}" || die "Compression failed for: ${f%%}"
			;;
		dir)
			tar --xattrs -${V}Scf - "${f%%}" -P | \
				$C >| "${f%%}.tar.${E}" || die "Compression failed for: ${f%%}"
			;;
		file)
			$C "${f%%}" || die "Compression failed for: ${f%%}"
			;;
	esac

	if [ "${orig_rm}" = "1" ];then rm -r "${f%%}";fi
}

orig_rm="0"
comp_dir="0"
comp_files="0"

V=""
comp_type="file"
mode="${0##*/mk}"

while getopts "BGXSLZdfsxzvh" OPT;do
	case "$OPT" in
		d) comp_dir="1";comp_type="dir";;
		f) comp_files="1";;
		s) orig_rm="1";;
		S) comp_dir="1";comp_type="status";;
		v) V="v";;
		x) comp_dir="1";orig_rm="1";;
		z) comp_files="1";orig_rm="1";comp_type="dir";;
		B) mode="bz2";;
		G) mode="gz";;
		L) mode="lz4";;
		X) mode="xz";;
		Z) mode="zst";;
		h)
			printf " default will compress files passed in \$1\n"
			printf " -d\tcompress all directories\n"
			printf " -f\tcompress all files\n"
			printf " -h\tprint this help\n"
			printf " -s\tcompress \$1, delete after compressed\n"
			printf " -S\tenable cool status bar, directories only\n"
			printf " -v\tenable verbose tar\n"
			printf " -x\tcompress all files, delete original after compressed\n"
			printf " -z\tcompress all directories, delete original after compressed\n"
			printf "\nForce MODES\n"
			printf " -B\tuse bzip2\n"
			printf " -G\tuse gzip\n"
			printf " -L\tuse lz4\n"
			printf " -X\tuse xz\n"
			printf " -Z\tuse zstd\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done
shift $((OPTIND - 1))

#$C compression command
#$E file extension
case "${mode}" in
	bz2)
		C="bzip2 -k"
		E="bz2"
		;;
	lz4)
		C="lz4 -k"
		E="lz4"
		;;
	gz)
		C="gzip -k"
		E="gz"
		;;
	xz)
		C="xz -k -e9"
		E="xz"
		;;
	zst)
		C="zstd -T0"
		E="zst"
		;;
esac

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
		if [ "${comp_dir}" = "1" ] && [ -d "${f}" ];then compress;fi
		if [ "${comp_files}" = "1" ] && [ -f "${f}" ];then compress;fi
	done
else
	printf "Nothing to compress\n";exit
fi
