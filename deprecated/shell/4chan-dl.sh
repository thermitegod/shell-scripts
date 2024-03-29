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
# 3.2.0
# 2020-04-25


die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }

dl(){ chandl -d "${save}" -t 32 -url "${link_get}"; }

dl_batch()
{
	if [ -n "$(echo "${board}"|grep '\#')" ];then return;fi #skip comments
	if [ -n "$(echo "${board}"|grep 'stop')" ];then exit;fi #exit when 'stop' is read as first argument
	url="https://boards.4chan.org/${board}/thread"
	link_get="${url}/${thread}"
	save="${dir}/${board}/${save_dir}"
	#printf "Downloading %s %s %s\n" "${board}" "${thread}" "${save_dir}"
	dl
}

mode="${0##*/}"
if [ "${mode}" = "4chan-dl" ];then
	thread_list="${XDG_DATA_HOME}/shell/4chan-dl"
	dir="${XDG_DOWNLOAD_DIR}/chan/4chan"
else
	thread_list="${XDG_DATA_HOME}/shell/8chan-dl"
	dir="${XDG_DOWNLOAD_DIR}/chan/8chan"
fi

while getopts "beh" OPT;do
	case "$OPT" in
		b)
			while read -r board thread save_dir;do
				dl_batch
			done < "${thread_list}"
			exit;;
		e) $EDITOR "${thread_list}";exit;;
		h)
			printf "Example: %s <save dir> <link>\n" "${0}"
			printf " -b\trun batch file\n"
			printf " -e\tedit %s\n" "${thread_list}"
			printf " -h\tPrint this help\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

if [ -z "${1}" ] || [ -z "${2}" ];then printf "Example: %s <save dir> <link>\n" "${0}";exit;fi

save="${1}"
link_get="${2}"
dl

