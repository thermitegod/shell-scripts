# -*- coding: utf-8 -*-
# 2.5.0
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
import atexit
import os
import shutil
import sys
import tempfile
from pathlib import Path

from loguru import logger

from python.utils.execute import Execute
from python.utils.get_files import GetOnlyFiles
from python.utils.mimecheck import Mimecheck


class Convert:
    def __init__(self, args: argparse = None):
        atexit.register(self.remove_tmpdir)

        self.__tmpdir = Path(tempfile.mkdtemp())

        self.__inc_iso = False

        self.__input_files = None
        self.__files = False

        self.parse_args(args=args)

        GetOnlyFiles(function=self.convert_main, input_files=self.__input_files, only_files=self.__files)

    def remove_tmpdir(self):
        shutil.rmtree(self.__tmpdir)

    def convert_main(self, filename):
        basename = filename.rpartition('.')[0]
        ext = filename.rpartition('.')[-1]

        if ext == 'mkv':
            return

        if ext == 'iso' and self.__inc_iso:
            # TODO - test iso conversion
            input('Important, not tested but should work\n')

            Execute(f'extract {filename}')

            if not Path.exists(Path('VIDEO_TS')):
                print(f'missing VIDEO_TS iso dir from: {filename}')
                return
            os.chdir('VIDEO_TS')

            # TODO - convert to native python
            Execute(f'rm -- *BUP *IFO')
            Execute(f'find . -maxdepth 1 -type f -size +0k -size -5M -exec rm -- "{{}}" \\;')

            for v in Path(Path.cwd()).iterdir():
                iso_basename = str(v).rpartition('.')[0]
                Execute(f'ffmpeg -hide_banner -i "{v}" '
                        f'-c:a copy -c:v copy -c:s copy "{self.__tmpdir}/{basename}-{iso_basename}.mkv"')

            os.chdir('..')
            Execute(f'mv -- "{self.__tmpdir}/{basename}.mkv" "{Path.cwd()}"')
            Execute(f'rm -rf -- ./AUDIO_TS ./VIDEO_TS')

            return
        else:
            if not Mimecheck.check_if_video(filename=filename):
                return

            original = Path.cwd() / 'original'
            original.mkdir(parents=True, exist_ok=True)

            Execute(f'ffmpeg -hide_banner -i "{filename}" '
                    f'-c:a copy -c:v copy -c:s copy "{self.__tmpdir}/{basename}.mkv"')

            # Path.rename does not like crossing partitions
            Execute(f'mv -- "{self.__tmpdir}/{basename}.mkv" "{Path.cwd()}"')
            Execute(f'mv -- "{Path.cwd()}/{filename}" "{original}"')

    def parse_args(self, args):
        if args.iso:
            self.__inc_iso = True

        self.__input_files = args.input_files
        self.__files = args.files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_files',
                        action='store',
                        type=str,
                        nargs='*',
                        default=None,
                        help=argparse.SUPPRESS)
    parser.add_argument('-f', '--files',
                        action='store_true',
                        help='convert all files in cwd')
    parser.add_argument('-i', '--iso',
                        action='store_true',
                        help='')
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
