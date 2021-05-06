# -*- coding: utf-8 -*-
# 2.0.0
# 2021-05-06

# Copyright (C) 2020,2021 Brandon Zorn <brandonzorn@cock.li>
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

import argparse
import os
import sys

from loguru import logger

from python.utils.execute import Execute


class AnimeRss:
    def __init__(self):
        cron = False

        try:
            if os.environ['CRON_RUN']:
                cron = True
        except KeyError:
            pass

        Execute('flexget --logfile /dev/null  execute --tasks Anime --disable-tracking',
                to_stdout=cron)


def main():
    parser = argparse.ArgumentParser()
    debug = parser.add_argument_group('debug')
    debug.add_argument('-L', '--loglevel',
                       default='INFO',
                       metavar='LEVEL',
                       type=str.upper,
                       choices=['NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'VERBOSE', 'DEBUG', 'TRACE'],
                       help='Levels: %(choices)s')
    args = parser.parse_args()

    logger.remove()
    logger.add(sys.stdout, level=args.loglevel, colorize=True)

    AnimeRss()
