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
# 1.1.0
# 2019-05-27


printf "Time format 00:00:00.0\n"

read -r -p "Start: " vstart
read -r -p "End: " vend

#ffmpeg -hide_banner -ss "${vstart}" -i "${1}" -c:a copy -c:v copy -c:s copy -t "${vend}" "${1%.*}-cut.mkv"
ffmpeg -hide_banner -ss "${vstart}" -i "${1}" -c:a copy -c:v copy -c:s copy -t "${vend}" "${1%%.*}-cut.mkv"
