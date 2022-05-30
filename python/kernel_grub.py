#!/usr/bin/env python3

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
# 4.0.0
# 2021-05-06


import argparse
import shutil
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from loguru import logger

from utils.execute import Execute
from utils.hash_compare import HashCompare
from utils.root_check import RootCheck


class Grub:
    def __init__(self):
        with TemporaryDirectory() as tmpdir:
            cfg = 'grub.cfg'

            cfgold = Path() / '/boot/grub' / cfg
            cfgnew = Path() / tmpdir / cfg

            cmd = f'grub-mkconfig -o {cfgnew}'
            Execute(cmd)

            if not Path.is_file(cfgnew):
                logger.info('grub did not create new cfg file')
                raise SystemExit(1)

            if Path.exists(cfgold):
                if not HashCompare(cfgold, cfgnew).results():
                    Path.unlink(cfgold)
                    shutil.move(cfgnew, cfgold)
                else:
                    logger.info('No changes needed to grub.cfg')
            else:
                shutil.move(cfgnew, cfgold)


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

    RootCheck(require_root=True)

    logger.remove()
    logger.add(sys.stdout, level=args.loglevel, colorize=True)

    Grub()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
