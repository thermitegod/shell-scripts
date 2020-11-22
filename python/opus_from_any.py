# -*- coding: utf-8 -*-
# 2.2.0
# 2020-11-21

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
import atexit
import shutil
import tempfile
from pathlib import Path

from python.utils.execute import Execute
from python.utils.get_files import GetFiles
from python.utils.mimecheck import Mimecheck


class Convert:
    def __init__(self):
        atexit.register(self.remove_tmpdir)

        self.__tmpdir = Path(tempfile.mkdtemp())

        self.__inc_iso = False

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

    def run(self, args):
        GetFiles.get_only_files(function=self.convert_main, input_files=args.input_files, only_files=args.files)


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
    args = parser.parse_args()

    run = Convert()
    run.run(args)
