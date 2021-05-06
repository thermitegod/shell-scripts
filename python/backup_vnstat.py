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

import argparse
import datetime
import shutil
import sys
from pathlib import Path

from loguru import logger


class Backup:
    def __init__(self):
        time = datetime.datetime.now()
        year = str(time.year)
        month = str(time.month)
        day = str(time.day)

        db = 'vnstat.db'
        target_src = Path() / '/var/lib/vnstat' / db
        target_dst = Path() / '/mnt/data/backup/vnstat-database' / year / month / day / db

        target_dst.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(target_src, target_dst)


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

    Backup()

