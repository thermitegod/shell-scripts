#!/usr/bin/env python3
# 1.0.0
# 2021-08-04

# Copyright (C) 2021 Brandon Zorn <brandonzorn@cock.li>
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
import os
import shutil
import sys
from pathlib import Path

from loguru import logger

from python.utils.hash_compare import HashCompare
from python.utils.root_check import RootCheck


class Symlink:
    def __init__(self):
        os.chdir(Path.cwd() / 'sbin')
        for f in Path.cwd().iterdir():
            dst = Path() / '/usr/local/sbin' / f.name
            if dst.is_file():
                if not HashCompare(f, dst).results():
                    logger.info(f'unlinking {dst}')
                    dst.unlink()

            if not dst.is_file():
                logger.info(f'copying {f} to {dst}')
                shutil.copy(f, dst)


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

    RootCheck(require_root=True)

    Symlink()
