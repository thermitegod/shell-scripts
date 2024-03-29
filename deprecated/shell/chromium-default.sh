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
# 5.4.0
# 2019-09-25


die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }

if [ "$(id -u)" -eq 0 ];then die "Do not run as root";fi

finish(){ if [ -d "${data}" ];then rm --preserve-root -r "${data}";fi }

#ver="chromium"
ver="google-chrome-unstable"

#profile gets appended
profile_location="${HOME}/.config/chrome/${ver}"

mode="${0##*/chromium-}"
E="${mode}"

while getopts "e:g:dsch" OPT;do
	case "$OPT" in
		e) E="ex${OPTARG}";shift;;
		d) E="default";shift;;
		s) mode="sandbox";shift;;
		c) ver="chromium";shift;;
		g)
			case "${OPTARG}" in
				1) ver="google-chrome-unstable";;
				2) ver="google-chrome-beta";;
				3) ver="google-chrome";;
				*) die "Invalid, exiting"
			esac
			;;
		h)
			printf "INFO\n"
			printf "Main way of launching profiles is through symlinks to this script\n"
			printf "profile names must start with 'chromium-'\n"
			printf "ln -s %s chromium-<name-of-profile>\n" "${0}"
			printf "flags are mainly for testing\n"
			printf "\nPROFILES\n"
			printf " -d\tdefault\n"
			printf " -e #\tex#, where '#' is any number\n"
			printf " -s\tsandbox, all data deleted on close\n"
			printf "\nBROWSER, default is: %s\n" "${ver}"
			printf " -c\tchromium\n"
			printf " -g 1\tgoogle-chrome-unstable\n"
			printf " -g 2\tgoogle-chrome-beta\n"
			printf " -g 3\tgoogle-chrome\n"
			printf "\nGENERAL\n"
			printf " -h\tprint this help\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done
shift $((OPTIND - 1))

case "${ver}" in
	chromium) cachedir="chromium";;
	*) cachedir="chrome";;
esac

case "${mode}" in
	sandbox)
		trap 'exit 1' INT HUP QUIT TERM USR1
		trap finish EXIT
		data=$(mktemp -d)
		;;
	*)
		data="${profile_location}-${E}"
		;;
esac

"${ver}" --user-data-dir="${data}"

if ! [ "${mode}" = "sandbox" ];then
	cache="${XDG_CACHE_HOME}/${cachedir}/${data##*/}"
	if [ -d "${cache}" ];then sleep 3;rm -rf "${cache}";fi
fi
