#!/usr/bin/env sh
#1.2.0
#2019-05-17

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

die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }

if [ "$(id -u)" -ne 0 ];then die "Requires root, exiting.";fi

state="auto"
card=/sys/class/drm/card0/device/power_dpm_force_performance_level
while getopts "acplh" OPT;do
	case "$OPT" in
		c) printf "Current power state is: %s\n" "$(cat "${card}")";exit;;
		a) state="auto";;
		p) state="high";;
		l) state="low";;
		h)
			printf "SET STATE\n"
			printf " -a\tauto\n"
			printf " -p\thigh\n"
			printf " -l\tlow\n"
			printf "GENERAL\n"
			printf " -c\tget current power state\n"
			printf " -h\tPrint this help\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

if [ "$(cat "${card}")" = "${state}" ];then printf "state '%s' is already active\n" "${state}";exit;fi
printf "current state is '%s', switching state to '%s'\n" "$(cat "${card}")" "${state}"
echo "${state}" >| "${card}"
