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
# 4.4.0
# 2019-05-17


fork="0"
extra_args=""
batch_links="/tmp/ytdl-batch.txt"

dl()
{
	printf "downloading : %s\n" "${link}"
	youtube-dl \
		--geo-bypass \
		--no-overwrites \
		--no-call-home \
		--yes-playlist \
		--audio-format best \
		--audio-quality 0 \
		--no-check-certificate ${extra_args} \
		"${link}"
	printf "downloaded : %s\n" "${link}"
}

batch()
{
	c="1"
	while read -r link;do
		printf "\n"
		dl
		printf "finished line : %s\n" "${c}"
		c=$((c+1))
	done < "${batch_links}"
}

while getopts "abefrh" OPT;do
	case "$OPT" in
		a) extra_args="--extract-audio";;
		b) batch;exit;;
		e) $EDITOR ${batch_links};exit;;
		f) fork="1";;
		r) if [ -f "${batch_links}" ];then rm "${batch_links}";fi;exit;;
		h)
			printf " -a\tonly download audio\n"
			printf " -b\trun batch file\n"
			printf " -e\tedit batch file\n"
			printf " -f\tfork\n"
			printf " -h\tprint this help\n"
			printf " -r\tremove %s\n" "${batch_links}"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done
shift $((OPTIND - 1))

if [ -n "${1}" ];then
	link="${1}"
elif [ -z "${1}" ];then
	link=$(xclip -o)
fi

if [ -z "$(echo "${link}"|grep http)" ];then printf "%s : not a valid link\n" "${link}";exit;fi
if [ "${fork}" = "0" ];then
	dl
else
	dl >/dev/null 2>&1 &
fi
