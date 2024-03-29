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
# 4.5.0
# 2019-09-25


final()
{
	d="${1}"
	dest="${PWD}"
	case "${job_run}" in
		dir_check)
			find . -maxdepth 1 -type f -iname "*.${d}" -exec mkdir -p "${dest}/${d}" \; -quit
			;;
		loop_main)
			find . -maxdepth 1 -type f -iname "*.${d}" -exec mv -i -- "{}" "${dest}/${d}" \;
			;;
	esac
}

final_all()
{
	final jpg
	final png
	final gif
	final webm
	final mp4
	final zip
	final mkv
	final rar
}

job_run="dir_check"
final_all
job_run="loop_main"
final_all
