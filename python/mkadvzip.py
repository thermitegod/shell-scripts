# -*- coding: utf-8 -*-
# 1.4.0
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
from pathlib import Path

from python.utils.execute import Execute


class Optimize:
    def __init__(self, args: argparse = None):
        self.__verbose = False

        self.__size_start = 0
        self.__size_end = 0

        self.__cpu = os.cpu_count()

        self.run(args=args)

    def get_size(self, start: bool):
        size = sum(f.stat().st_size for f in Path.cwd().glob('**/*') if f.is_file())
        if start:
            self.__size_start = size
        else:
            self.__size_end = size

    def main(self):
        if self.__verbose:
            self.get_size(start=True)

        Execute(f'find . -type f -iname \'*.zip\' -print0 | '
                f'nice -19 xargs --max-args=1 --max-procs={self.__cpu} --null '
                f'advzip -z -4',
                sh_wrap=True)

        if self.__verbose:
            self.get_size(start=False)
            print(f'Before     : {self.__size_start}\n'
                  f'After      : {self.__size_end}\n'
                  f'% of orig  : {self.__size_end / self.__size_start}')

    def run(self, args):
        if args.verbose:
            self.__verbose = True

        self.main()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Print change in dir size')
    args = parser.parse_args()

    Optimize(args=args)
