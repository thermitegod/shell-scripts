#!/usr/bin/env sh
#1.1.0
#2019-05-27

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

printf "Time format 00:00:00.0\n"

read -r -p "Start: " vstart
read -r -p "End: " vend

#ffmpeg -hide_banner -ss "${vstart}" -i "${1}" -c:a copy -c:v copy -c:s copy -t "${vend}" "${1%.*}-cut.mkv"
ffmpeg -hide_banner -ss "${vstart}" -i "${1}" -c:a copy -c:v copy -c:s copy -t "${vend}" "${1%%.*}-cut.mkv"
