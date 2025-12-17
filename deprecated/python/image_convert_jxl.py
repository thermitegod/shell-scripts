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
# 2.1.0
# 2021-06-23


import argparse
import os
import shutil
import sys
from multiprocessing.dummy import Pool as ThreadPool
from pathlib import Path

from loguru import logger

from utils.execute import Execute
from utils.recursion import RecursiveExecuteThreadpool


class Convert:
    def __init__(self, args: argparse = None):
        os.nice(19)

        self.__orig = 'jxl_original'

        self.__error_counter = 0

        self.__rm_orig = False

        self.__jpeg_xl_supported_ext = ('.png', '.apng', '.gif', '.jpg', '.jpeg' '.exr', '.ppm', '.pfm', '.pgx')

        self.__jpeg_xl_speed = None

        self.parse_args(args=args)

    def convert_image(self, filename: Path):
        path = filename.parent
        filename_new = Path() / path / f'{filename.stem}.jxl'

        # Execute(f'cjxl --effort=1 "{filename}" "{filename_new}"')

        Execute(f'cjxl -d 1 --strip --effort={self.__jpeg_xl_speed} "{filename}" "{filename_new}"')

        # --keep_invisible=1

        # Execute(f'cjxl --effort={self.__jpeg_xl_speed} "{filename}" "{filename_new}"')

        # Execute(f'cjxl --strip --keep_invisible=1 --extra-properties=3 '
        #         f'--effort={self.__jpeg_xl_speed} "{filename}" "{filename_new}"')

        if Path.is_file(filename_new):
            orig = path / self.__orig
            if not Path.is_dir(orig):
                orig.mkdir(parents=True, exist_ok=True)
            Path.rename(filename, orig / filename.name)
        else:
            logger.error(f'Missing: {filename_new}')
            self.__error_counter += 1

    def convert_main(self, path: Path = None):
        if path.name == self.__orig:
            # prevents recursion if run again
            return

        orig = path / self.__orig

        filenames = [f for f in path.iterdir()
                     if f.is_file() and
                     f.suffix in self.__jpeg_xl_supported_ext]

        threadpool = ThreadPool(os.cpu_count())
        threadpool.map(self.convert_image, filenames)
        threadpool.close()
        threadpool.join()

        if Path.exists(orig):
            c1 = 0  # original
            c2 = 0  # converted
            for f in Path(orig).iterdir():
                if f.is_file():
                    c1 += 1
            for f in path.iterdir():
                if f.is_file():
                    c2 += 1

            if c1 != c2:
                logger.error(f'total file count does not match: {c1}, {c2} in \'{path}\'')
                self.__error_counter += 1
                return
            else:
                logger.debug(f'counters match in \'{path}\'')

            if self.__rm_orig:
                if Path.is_dir(orig):
                    logger.debug(f'removing original: {orig}')
                    shutil.rmtree(orig)
                else:
                    logger.error(f'missing dir: {orig}')

    def parse_args(self, args):
        if not args.disable_warning:
            for f in range(10):
                logger.warning(f'JPEG-XL standard is still in progress')

            logger.warning(f'')
            logger.warning(f'')
            logger.warning(f'use -W to bypass this')
            raise SystemExit

        # jpeg-xl
        if args.speed:
            self.__jpeg_xl_speed = args.speed[0]

        if args.rm_orig:
            self.__rm_orig = True

        if args.mimecheck:
            Execute('mime-correct')

        if args.convert_all:
            RecursiveExecuteThreadpool(function=self.convert_main)
        else:
            self.convert_main(path=Path.cwd())

        if self.__error_counter > 0:
            logger.error(f'Errors encountered durring conversion')
            logger.error(f'Error count is: {self.__error_counter}')


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
                        help='run mime check and correction')

    general = parser.add_argument_group('jpeg-xl')
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


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
