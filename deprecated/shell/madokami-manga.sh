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
# 7.9.0
# 2019-09-25


dl()
{
	wget \
		--random-wait \
		--recursive \
		--level=2 \
		-e robots=off \
		--no-parent \
		--timestamping \
		--max-redirect 0 \
		--no-host-directories \
		--cut-dirs=4 \
		--accept zip,7z,rar,cbr,cbz,pdf,epub,mobi \
		--directory-prefix="${save}" \
		--user "${mado_user}" \
		--password "${mado_pass}" \
		--hsts-file=/tmp/wget-hsts \
		"${link}"
}

publishing(){ while read -r link;do dl;done < "${links}"; }

. "$(dirname "$0")/utils.sh"
. "${extra}/madokami-user-pass.sh" # exports $mado_user $mado_pass

symlink="0"
symdir="${HOME}/media/manga-reading"
d="/mnt/data/manga"
save="${d}/neglected/in-print"

mangalinks="${extra}/madokami-manga"
novellinks="${extra}/madokami-novels"

mode="${0##*/}";mode="${mode%%.sh}"
while getopts "dleh" OPT;do
	case "$OPT" in
		d) save="${d}/neglected/finished";;
		l) symlink="1";;
		e) "$EDITOR" "${extra}/madokami-manga";exit;;
		h)
			printf " -e\tedit %s/madokami-manga\n" "${extra}"
			printf " -d\tsave to %s/neglected/finished\n" "${d}"
			printf " -h\tprint this help\n"
			printf " -l\tsymlink to %s\n" "${symdir}"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done
shift $((OPTIND - 1))

case "${mode}" in
	madokami-manga)
		if [ -n "${1}" ];then
			link="${1}"
		elif [ -z "${1}" ];then
			link=$(xclip -o)
		fi
		printf "downloading: %s\n" "${link}"
		dl
		printf "downloaded: %s\n" "${link}"
		w="${link##*/}"
		x=$(echo "${w}"|sed -e 's/%20/ /g')
		printf "save path: %s/%s\n" "${save}" "${x}"
		if [ "${symlink}" = "1" ];then ln -sv "${save}/${x}" "${symdir}/${x}";fi
		;;
	madokami-manga-publishing)
		links="${mangalinks}"
		publishing
		;;
	madokami-novels-publishing)
		save="${d}/novel"
		links="${novellinks}"
		publishing
		;;
esac
