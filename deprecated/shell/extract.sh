#!/usr/bin/env sh

# Copyright (C) ???? Unknown
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
# 1.7.1
# 2020-05-12


while true;do
	if [ -f "${1}" ];then
		case "${1}" in
			*.tgz|*.tbz2) tar xvf "${1}";break;;
			*.txz) tar xvJf "${1}";break;;
			*.tar.bz2) tar xvjf "${1}";break;;
			*.tar.gz) tar xvzf "${1}";break;;
			*.tar.xz) tar xvJf "${1}";break;;
			*.tar.zst) zstd -dc --long=31 "${1}"|tar xvf -;break;;
			*.tar.lz4) lz4 -dc "${1}"|tar xvf -;break;;
			*.tar.lzma) tarlzma xvf "${1}";break;;
			*.tar.lrz) lrzuntar "${1}";break;;
			*.rar|*.RAR) unrar "${1}";break;;
			*.gz) gunzip -k "${1}";break;;
			*.xz) unxz -k "${1}";break;;
			*.bz2) bzip2 -dk "${1}";break;;
			*.zst) unzstd -d --long=31 "${1}";break;;
			*.tar) tar xvf "${1}";break;;
			*.zip) unzip "${1}";break;;
			*7z|*.iso|*.ISO) 7z x "${1}";break;;
			*.cbz|*.cbr) 7z x "${1}" -o"${1}";break;;
			*) printf "cannot extract: %s\n" "${1}";break;;
		esac
	else
		printf "not a valid file: %s\n" "${1}"
	fi
	if [ -n "${2}" ];then shift;else break;fi
done
