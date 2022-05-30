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
# 3.3.0
# 2019-09-25


finish(){ if [ -d "${tmpdir}" ];then rm --preserve-root -r "${tmpdir}";fi }
trap 'exit 1' INT HUP QUIT TERM USR1
trap finish EXIT
tmpdir=$(mktemp -d)

i="$(date +%s).png"
mode="${0##*/}"
case "${mode}" in
	snip)
		gm import "${tmpdir}/${i}"
		;;
	snip-root)
		gm import -window root "${tmpdir}/${i}"
		;;
esac
#nice -19 optipng -o7 -strip all "${tmpdir}/${i}">/dev/null 2>&1
mv "${tmpdir}/${i}" "${HOME}"
