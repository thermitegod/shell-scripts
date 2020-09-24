#!/usr/bin/env python3
# 1.0.0
# 2020-09-18

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

from utils import mimecheck
from utils import utils


class Convert:
    def __init__(self):
        atexit.register(self.remove_tmpdir)

        self.__tmpdir = Path(tempfile.mkdtemp())

        self.__files = False
        self.__inc_iso = False

        self.__input_files = None

    def remove_tmpdir(self):
        shutil.rmtree(self.__tmpdir)

    def convert_main(self, filename):
        basename = filename.rpartition('.')[0]
        ext = filename.rpartition('.')[-1]

        if ext == 'opus':
            return

        if not mimecheck.check_if_video(filename=filename) or \
                not mimecheck.check_if_audio(filename=filename):
            return

        original = Path.cwd() / 'original'
        original.mkdir(parents=True, exist_ok=True)

        utils.run_cmd(f'ffmpeg -hide_banner -i "{filename}" '
                      f' -acodec libopus -b:a 128k -vbr on -compression_level 10 '
                      f'-map_metadata 0 -id3v2_version 3 "{self.__tmpdir}/{basename}.opus"')

        # Path.rename does not like crossing partitions
        utils.run_cmd(f'mv -- "{self.__tmpdir}/{basename}.opus" "{Path.cwd()}"')
        utils.run_cmd(f'mv -- "{Path.cwd()}/{filename}" "{original}"')

    def get_files(self):
        if self.__files:
            dir_listing = []
            for f in Path(Path.cwd()).iterdir():
                dir_listing.append(str(f))

            for f in dir_listing:
                if Path.is_file(Path(f)) and self.__files:
                    self.convert_main(filename=f)
        elif self.__input_files is not None:
            for f in self.__input_files:
                if Path.is_file(Path(f)):
                    self.convert_main(filename=f)

    def run(self, args):
        if args.files:
            self.__files = True
        if args.input_files is not None:
            self.__input_files = args.input_files

        self.get_files()


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


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
