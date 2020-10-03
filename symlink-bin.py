#!/usr/bin/env python3
# 1.0.0
# 2020-10-02

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

import argparse
import os
from pathlib import Path

from utils import utils


class Symlink:
    def __init__(self):
        # since root is req to do this Path.home() will return
        # /root so create wanted home path
        self.__user = 'brandon'

        self.__home_bin = Path() / '/home' / self.__user / '.bin'
        self.__local_bin = Path() / '/usr/local/bin'

        self.__ignore = '--ignore=".git" --ignore=".gitignore"'

    def run(self, args):
        # decompression type
        if args.stow_bin:
            os.chdir(self.__home_bin)
            utils.run_cmd(f'stow {self.__ignore} -v --target={self.__local_bin} bin bin-other opt')
        if args.unstow_bin:
            os.chdir(self.__home_bin)
            utils.run_cmd(f'stow {self.__ignore} -D -v --target={self.__local_bin} bin bin-other opt')


def main():
    parser = argparse.ArgumentParser()
    stow = parser.add_argument_group('STOW')
    stow.add_argument('-b', '--stow-bin',
                      action='store_true',
                      help='')
    unstow = parser.add_argument_group('UNSTOW')
    unstow.add_argument('-B', '--unstow-bin',
                        action='store_true',
                        help='')
    args = parser.parse_args()

    utils.args_required_else_help()

    utils.root_check(require_root=True)

    run = Symlink()
    run.run(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
