# -*- coding: utf-8 -*-
# 1.2.0
# 2021-04-29

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
import shutil
import sys
from pathlib import Path

from loguru import logger

from python.utils.execute import Execute
from python.utils.mimecheck import Mimecheck
from python.utils.recursion import RecursiveExecute


class Convert:
    def __init__(self, args: argparse = None):
        self.__rm_orig = False
        self.__mimecheck = True

        self.__jpeg_xl_supported_ext = ('.png', '.apng', '.gif', '.jpg', '.jpeg' '.exr', '.ppm', '.pfm', '.pgx')

        self.__jpeg_xl_binary = None
        self.__jpeg_xl_speed = None

        self.run(args=args)

    def convert_main(self):
        orig = Path.cwd() / 'orig'
        if not Path.is_dir(orig):
            # need this check for RecursiveExecute()
            if str(orig.parent).endswith('orig'):
                return
            orig.mkdir(parents=True, exist_ok=True)

        c1 = 0
        c2 = 0

        if self.__mimecheck:
            Execute('mime-correct')

        for filename in Path.cwd().iterdir():
            if Path.is_dir(filename):
                continue

            if Mimecheck.check_if_image(filename=filename):
                filename_base = filename.stem
                filename_ext = filename.suffix

                if filename_ext not in self.__jpeg_xl_supported_ext:
                    continue

                Execute(f'{self.__jpeg_xl_binary} -s {self.__jpeg_xl_speed} -E 3 {filename.name} {filename_base}.jxl')
                Path.rename(filename, Path() / orig / filename.name)
                c1 += 1

        if Path.exists(orig):
            for f in Path.cwd().iterdir():
                if f.is_file():
                    c2 += 1

            if c1 != c2:
                logger.error(f'total file count does not match: {c1}, {c2} in \'{Path.cwd()}\'')
                raise SystemExit

            if self.__rm_orig:
                logger.debug(f'Removing Original: {orig}')
                shutil.rmtree(orig)

    def run(self, args):
        if not args.disable_warning:
            for f in range(10):
                logger.warning(f'JPEG-XL standard is still in progress')

            logger.warning(f'')
            logger.warning(f'')
            logger.warning(f'use -W to bypass this')
            raise SystemExit

        # jpeg-xl
        if args.binary:
            self.__jpeg_xl_binary = Path(args.binary[0])

        if args.speed:
            self.__jpeg_xl_speed = args.speed[0]

        if args.rm_orig:
            self.__rm_orig = True

        if args.mimecheck:
            self.__mimecheck = False

        if args.convert_all:
            RecursiveExecute(function=self.convert_main)
        else:
            self.convert_main()


def main():
    parser = argparse.ArgumentParser()

    general = parser.add_argument_group('general')
    general.add_argument('-A', '--convert-all',
                         action='store_true',
                         help='run in all sub-dirs of CWD')
    general.add_argument('-r', '--rm-orig',
                         action='store_true',
                         help='do not keep original images')
    general.add_argument('-W', '--disable-warning',
                         action='store_true',
                         help='disable warning about the jpeg-xl standard')

    modify = parser.add_argument_group('file modification')
    modify.add_argument('-m', '--mimecheck',
                        action='store_true',
                        help='disable mime check and correction')

    general = parser.add_argument_group('jpeg-xl')
    general.add_argument('-b', '--binary',
                         default=['/home/brandon/projects/jpeg-xl/build/tools/cjxl'],
                         metavar='BINARY',
                         nargs=1,
                         help='location of jpeg-xl binary \'cjxl\'')
    general.add_argument('-s', '--speed',
                         default=['9'],
                         metavar='SPEED',
                         nargs=1,
                         help='Encoder effort/speed setting.')

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

    Convert(args=args)
