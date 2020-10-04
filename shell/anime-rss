#!/usr/bin/env sh
#2.2.0
#2020-04-25

# Copyright (C) 2018,2019,2020 Brandon Zorn <brandonzorn@cock.li>
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

if [ -n "$(pstree -s $$|grep cron)" ];then
	flexget-headless --cron execute --tasks Anime --disable-tracking
else
	flexget-headless --logfile /dev/null  execute --tasks Anime --disable-tracking
fi
