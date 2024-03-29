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
# 2018-02-08


#TODO
#print tracks
#promt for tracks instead of hard coded

mkdir -p ./old
mv ./*.mkv ./old
cd ./old

#map index starts at 0
for f in *.mkv;do
	ffmpeg -hide_banner -i "${f}" -map 0:0 -map 0:2 -map 0:3 -c:v copy -c:a copy -c:s copy ../"${f}"
done
