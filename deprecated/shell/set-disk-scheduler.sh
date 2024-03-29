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
# 2.3.0
# 2019-09-25


die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }

if [ "$(id -u)" -ne 0 ];then die "Requires root, exiting.";fi

debug="0"
sched="mq-deadline"

pool_storage="sda sdb sdc sdd sde sdf sdg sdh sdk sdi sdm sdn"
pool_torrents="sdm sdn"
pool_ssd="sdl sdj"
pool_root="nvme0n1 nvme1n1"
disks="$(echo "${pool_storage}" "${pool_torrents}" "${pool_ssd}" "${pool_root}")"

if [ -z "${1}" ];then "${0}" -h;exit;fi
while getopts "dpsh" OPT;do
	case "$OPT" in
		d) debug="1";;
		p) mode="print";;
		s) mode="set";;
		h)
			printf " -d\trun with debug printouts\n"
			printf " -h\tprint this help\n"
			printf " -p\tPrint current scheduler\n"
			printf " -s\tset disk scheduler\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

#do not quote
for f in ${disks};do
	case "${mode}" in
		set)
			echo $sched >| "/sys/block/${f}/queue/scheduler"
			if [ "${debug}" = "1" ];then printf "scheduler set to [%s] for /sys/block/%s\n" "${sched}" "${f}";fi
			;;
		print)
			printf "Scheduler is \"$(cat "/sys/block/${f}/queue/scheduler")\" for %s\n" "${f}"
			;;
	esac
done
