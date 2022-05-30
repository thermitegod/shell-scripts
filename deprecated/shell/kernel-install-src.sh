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
# 2.7.0
# 2019-09-15


die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }

if [ "$(id -u)" -ne 0 ];then die "Requires root, exiting.";fi

pkg="sys-kernel/gentoo-sources"
v="--quiet"
while getopts "Vvgh" OPT;do
	case "$OPT" in
		V) v="--verbose";;
		g) pkg="sys-kernel/git-sources";;
		v) pkg="sys-kernel/vanilla-sources";;
		h)
			printf "GENERAL\n"
			printf " -h\tPrint this help\n"
			printf " -V\tverbose emerge\n"
			printf "\nKERNELS: defaults is sys-kernel/gentoo-sources\n"
			printf " -g\tinstall sys-kernel/git-sources\n"
			printf " -v\tinstall sys-kernel/vanilla-sources\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

emerge --ignore-default-opts --oneshot "$v" "$pkg" || die "somethings broken"

if [ -f "/proc/config.gz" ];then
	printf "Installing running kernel config\n"
	zcat /proc/config.gz >| /usr/src/linux/.config
fi
