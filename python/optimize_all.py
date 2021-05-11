# -*- coding: utf-8 -*-
# 1.9.0
# 2021-04-29

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
import os
import sys
from pathlib import Path

from loguru import logger

from python.utils.check_env import CheckEnv
from python.utils.execute import Execute


class Optimize:
    def __init__(self, args: argparse = None):
        self.__verbose = False
        self.__disable_mimecheck = False
        self.__mode = CheckEnv.get_script_name()
        self.__png_max = False
        self.__png_oxipng = True

        self.__size_start = 0
        self.__size_end = 0

        self.__cpu = os.cpu_count()

        self.parse_args(args=args)

        self.main()

    def get_size(self, start: bool):
        size = sum(f.stat().st_size for f in Path.cwd().glob('**/*') if f.is_file())
        if start:
            self.__size_start = size
        else:
            self.__size_end = size

    def optimize_jpg(self):
        Execute(f'find . -type f -iname \'*.jp**\' -print0 | '
                f'nice -19 xargs --max-args=1 --max-procs={self.__cpu} --null '
                f'jpegoptim --strip-all --preserve --preserve-perms',
                sh_wrap=True)

    def optimize_png(self):
        if self.__png_oxipng:
            # use oxipng
            level = 'max'

            Execute(f'find . -type f -iname \'*.png\' -print0 | '
                    f'nice -19 xargs --max-args=1 --max-procs={int(self.__cpu / 4)} --null '
                    f'oxipng --threads {int(self.__cpu / 2)} -o {level} --strip all --preserve',
                    sh_wrap=True)
        else:
            # use optipng
            level = '5'
            if self.__png_max:
                level = '7'

            Execute(f'find . -type f -iname \'*.png\' -print0 | '
                    f'nice -19 xargs --max-args=1 --max-procs={self.__cpu} --null '
                    f'optipng -o{level} -strip all -preserve',
                    sh_wrap=True)

    def optimize_gif(self):
        Execute(f'find . -type f -iname \'*.gif\' -print0 | '
                f'nice -19 xargs --max-args=1 --max-procs={self.__cpu} --null '
                f'gifsicle -bO3 -V',
                sh_wrap=True)

    def main(self):
        if self.__verbose:
            self.get_size(start=True)

        if not self.__disable_mimecheck:
            Execute('mime-correct -A')

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
            print(f'Before     : {self.__size_start}\n'
                  f'After      : {self.__size_end}\n'
                  f'% of orig  : {self.__size_end / self.__size_start}')

    def parse_args(self, args):
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
                        choices=['jpg', 'png', 'gif', 'all'],
                        help='Which file to optimize [all]')
    parser.add_argument('-x', '--png-max',
                        action='store_true',
                        help='optipng only, use -o7 instead of -o5')
    parser.add_argument('-z', '--png-optipng',
                        action='store_true',
                        help='use optipng instead of oxipng')
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

    Optimize(args=args)
