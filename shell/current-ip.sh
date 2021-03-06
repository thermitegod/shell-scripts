#!/usr/bin/env sh
#2.11.0
#2019-03-11

# Copyright (C) 2018,2019,2020 Brandon Zorn <brandonzorn@cock.li>
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

mode="once"
d="${HOME}/documents/internet"

while getopts "dhk" OPT;do
	case "$OPT" in
		d) mode="daily";;
		k) if ! [ -d "${d}" ];then mkdir -p "${d}";fi;;
		h)
			printf " -d\tdaily files timestamped\n"
			printf " -h\tPrint this help\n"
			printf " -k\tcreate storage dir: %s\n" "${d}"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

date_day="$(date "+%F")"
date_time="$(date "+%H:%M:%S")"
ip="$(curl --max-time 30 --silent ifconfig.co)"
if [ "$(echo "${ip}"|grep Error)" ];then ip="INTERNAL ERROR"
elif [ -z "${ip}" ];then ip="DOWN"
fi

case "$mode" in
	daily) echo "${date_day} ${date_time} : ${ip}" >> "${d}/${date_day}.txt";;
	once) echo "${date_day}" "${date_time}" : "${ip}";;
esac
