#!/usr/bin/env python3
# 1.4.1
# 2020-10-04

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
import sys
import os
from pathlib import Path

from loguru import logger

from utils import utils


class Optimize:
    def __init__(self):
        self.__verbose = False
        self.__disable_mimecheck = False
        self.__mode = utils.get_script_name()
        self.__png_max = False
        self.__png_oxipng = True

        self.__size_start = 0
        self.__size_end = 0

        self.__cpu = os.cpu_count()

    def get_size(self, start: bool):
        size = sum(f.stat().st_size for f in Path.cwd().glob('**/*') if f.is_file())
        if start:
            self.__size_start = size
        else:
            self.__size_end = size

    def optimize_jpg(self):
        utils.run_cmd(f'find . -type f -iname \'*.jp**\' -print0 | '
                      f'nice -19 xargs --max-args=1 --max-procs={self.__cpu} --null '
                      f'jpegoptim --strip-all --preserve --preserve-perms',
                      sh_wrap=True)

    def optimize_png(self):
        if self.__png_oxipng:
            # use oxipng
            level = 'max'

            utils.run_cmd(f'find . -type f -iname \'*.png\' -print0 | '
                          f'nice -19 xargs --max-args=1 --max-procs={int(self.__cpu / 4)} --null '
                          f'oxipng --threads {int(self.__cpu / 2)} -o {level} --strip all --preserve',
                          sh_wrap=True)
        else:
            # use optipng
            level = '5'
            if self.__png_max:
                level = '7'

            utils.run_cmd(f'find . -type f -iname \'*.png\' -print0 | '
                          f'nice -19 xargs --max-args=1 --max-procs={self.__cpu} --null '
                          f'optipng -o{level} -strip all -preserve',
                          sh_wrap=True)

    def optimize_gif(self):
        utils.run_cmd(f'find . -type f -iname \'*.gif\' -print0 | '
                      f'nice -19 xargs --max-args=1 --max-procs={self.__cpu} --null '
                      f'gifsicle -bO3 -V',
                      sh_wrap=True)

    def main(self):
        if self.__verbose:
            self.get_size(start=True)

        if not self.__disable_mimecheck:
            utils.run_cmd('mime-correct -A')

        if self.__mode == 'optimize-all':
            self.optimize_gif()
            self.optimize_jpg()
            self.optimize_png()
        elif self.__mode == 'optimize-jpg':
            self.optimize_jpg()
        elif self.__mode == 'optimize-png':
            self.optimize_png()
        elif self.__mode == 'optimize-gif':
            self.optimize_gif()

        if self.__verbose:
            self.get_size(start=False)
            print(f'Before     : {self.__size_start}')
            print(f'After      : {self.__size_end}')
            print(f'% of orig  : {self.__size_end / self.__size_start}')

    def run(self, args):
        if args.verbose:
            self.__verbose = True
        if args.disable_mimecheck:
            self.__disable_mimecheck = True
        if args.mode_force:
            self.__mode = f'optimize-{args.mode_force}'
        if args.png_max:
            self.__png_max = True
        if args.png_optipng:
            self.__png_oxipng = False

        self.main()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Print change in dir size')
    parser.add_argument('-M', '--disable-mimecheck',
                        action='store_true',
                        help='disanle mime check')
    parser.add_argument('-m', '--mode-force',
                        metavar='MODE',
                        type=str,
                        nargs=1,
                        choices=['jpg', 'png', 'gif', 'all'],
                        help='Which file to optimize [all]')
    parser.add_argument('-x', '--png-max',
                        action='store_true',
                        help='optipng only, use -o7 instead of -o5')
    parser.add_argument('-z', '--png-optipng',
                        action='store_true',
                        help='use optipng instead of oxipng')
    debug = parser.add_argument_group('DEBUG')
    debug.add_argument('-L', '--loglevel',
                       default='INFO',
                       metavar='LEVEL',
                       type=str.upper,
                       choices=['NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'VERBOSE', 'DEBUG', 'TRACE'],
                       help='Levels: %(choices)s')
    args = parser.parse_args()

    logger.remove()
    logger.add(sys.stdout, level=args.loglevel, colorize=True)

    run = Optimize()
    run.run(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
