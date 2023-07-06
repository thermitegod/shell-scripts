#!/usr/bin/env python3

# Copyright (C) 2018-2023 Brandon Zorn <brandonzorn@cock.li>
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
# 6.0.0
# 2023-07-05


import argparse
import os
import sys
import time
from pathlib import Path

from loguru import logger

from utils.check_env import CheckEnv
from utils.execute import Execute


class Snip:
    def __init__(self):
        self.__is_display_server_wayland = False
        try:
            if os.environ['WAYLAND_DISPLAY']:
                self.__is_display_server_wayland = True
        except KeyError:
            pass

        snip_path = f'{Path.home()}/{int(time.time())}.png'

        if self.__is_display_server_wayland:
            if CheckEnv.get_script_name() == 'snip-root':
                Execute(f'grimshot save screen {snip_path}')
            else:
                Execute(f'grimshot save area {snip_path}')
        else:
            if CheckEnv.get_script_name() == 'snip-root':
                Execute(f'gm import -window root {snip_path}')
            else:
                Execute(f'gm import {snip_path}')


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

    Snip()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
