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
# 2019-05-27


ls -1A
read -r -p "Current Extension: " extold

if [ "${extold}" = "cbr" ];then
	extnew="rar"
elif [ "${extold}" = "cbz" ];then
	extnew="zip"
else
	read -r -p "New Extension: " extnew
fi

printf "Changing *.%s to *.%s\n" "${extold}" "${extnew}"
read -r -p "Confirm rename [yn] " confirm

if echo "${confirm}" | grep -iq "^y";then
	for f in *."${extold}";do
		mv "${f}" "${f%.*}.${extnew}"
	done
else
	printf "Not running"
fi

