#!/usr/bin/env sh
#2.1.0
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

file_count()
{
	cnt="$(find "${D}" -maxdepth 1 -type f -size +"${lower}" -size -"${upper}" | wc -l)"
	if ! [ "${cnt}" = "0" ];then printf "%s-%s  \t: %s\n" "${lower}" "${upper}" "${cnt}";fi
	unset cnt lower upper
}

if [ -n "${1}" ];then D="${1}";else D=".";fi

lower="0k"
upper="10M"
file_count

lower="10M"
upper="100M"
file_count

lower="100M"
upper="150M"
file_count

lower="150M"
upper="200M"
file_count

lower="200M"
upper="500M"
file_count

lower="500M"
upper="1G"
file_count

lower="1G"
upper="10G"
file_count

lower="10G"
upper="100G"
file_count
