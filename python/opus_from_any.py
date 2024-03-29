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
# 2.5.0
# 2021-04-29


import argparse
import atexit
import shutil
import sys
import tempfile
from pathlib import Path

from loguru import logger

from utils.execute import Execute
from utils.get_files import GetOnlyFiles
from utils.mimecheck import Mimecheck


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

        if ext == 'opus':
            return

        if not Mimecheck.check_if_video(filename=filename) or \
                not Mimecheck.check_if_audio(filename=filename):
            return

        original = Path.cwd() / 'original'
        original.mkdir(parents=True, exist_ok=True)

        Execute(f'ffmpeg -hide_banner -i "{filename}" '
                f' -acodec libopus -b:a 128k -vbr on -compression_level 10 '
                f'-map_metadata 0 -id3v2_version 3 "{self.__tmpdir}/{basename}.opus"')

        # Path.rename does not like crossing partitions
        Execute(f'mv -- "{self.__tmpdir}/{basename}.opus" "{Path.cwd()}"')
        Execute(f'mv -- "{Path.cwd()}/{filename}" "{original}"')

    def parse_args(self, args):
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
