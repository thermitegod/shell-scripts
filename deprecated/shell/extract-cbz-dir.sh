#!/usr/bin/env sh
#2.0.0
#2017-11-10

# Copyright (C) 2018 Brandon Zorn <brandonzorn@cock.li>
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

for f in *; do
	if [ -f "${f%.*}.cbz" ];then
		nice -19 7z x "${f%%}" -o"*"
	fi

	if [ -f "${f%.*}.cbr" ];then
		#7z errors out on some cbr files, using unrar
		x_dir=$(echo "${f}"|sed "s/.[^.]*$//")
		#echo $x_dir
		mkdir -pv "${x_dir}"
		nice -19 unrar x "${f%%}" ./"${x_dir}"
	fi
done
