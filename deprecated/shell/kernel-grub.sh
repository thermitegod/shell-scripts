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
# 2.2.1
# 2019-09-27


die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }

if [ "$(id -u)" -ne 0 ];then die "Requires root, exiting.";fi

finish(){ if [ -d "${tmpdir}" ];then rm --preserve-root -r "${tmpdir}";fi; }
trap 'exit 1' INT HUP QUIT TERM USR1
trap finish EXIT
tmpdir=$(mktemp -d)

cfgold="/boot/grub/grub.cfg"
cfgnew="${tmpdir}/grub.cfg"
. "$(dirname "$0")/colors.sh"

grub-mkconfig -o "${cfgnew}"
if ! [ -f "${cfgnew}" ];then die "grub did not create new cfg file\n";fi
if ! [ "$(openssl sha1 "${cfgold}"|awk '{print $2}')" = "$(openssl sha1 ${cfgnew}|awk '{print $2}')" ];then
	rm "${cfgold}"
	mv "${cfgnew}" "${cfgold}"
fi
