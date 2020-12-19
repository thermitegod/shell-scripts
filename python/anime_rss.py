# -*- coding: utf-8 -*-
# 1.0.0
# 2020-12-19

# Copyright (C) 2020 Brandon Zorn <brandonzorn@cock.li>
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

# crontab entry
# 0 *	*	*	*	CRON_RUN=1 /usr/local/bin/anime-rss

import os

from python.utils.execute import Execute


def main():
    try:
        cron = bool(os.environ['CRON_RUN'])
    except KeyError:
        cron = False

    Execute('flexget --logfile /dev/null  execute --tasks Anime --disable-tracking',
            to_stdout=cron)
