#!/usr/bin/env sh
#3.3.0
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

if [ -z "${1}" ];then "${0}" -h;exit;fi
while getopts "123456hrc" OPT;do
	case "$OPT" in
		1) h="sha1";;
		2) h="sha224";;
		3) h="sha256";;
		4) h="sha384";;
		5) h="sha512";;
		6) h="md5";;
		c) mode="checksum";;
		r) mode="rename-checksum";;
		h)
			printf "ALGOS\n"
			printf " -1\tsha1\n"
			printf " -2\tsha224\n"
			printf " -3\tsha256\n"
			printf " -4\tsha384\n"
			printf " -5\tsha512\n"
			printf " -6\tmd5\n"
			printf "GENERAL\n"
			printf " -h\tprint this help\n"
			printf "FORCE MODE\n"
			printf " -c\tforce checksum\n"
			printf " -r\tforce rename\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

mode="${0##*/}"
case "${mode}" in
	checksum)
		find . -type f -print0 | nice -19 xargs --max-args=1 --max-procs=$(($(nproc)+1)) --null openssl ${h}
		;;
	rename-checksum)
		for f in *;do
			if [ -f "${f}" ];then openssl "${h}" "${f}" | sed -e 's/\([^ ]*\) \(.*\(\..*\)\)$/mv -v \2 \1\3/e';fi
		done
		;;
esac

