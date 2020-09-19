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
import mimetypes
import shutil
import os
import tempfile
from pathlib import Path

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

    @staticmethod
    def check_if_video(filename):
        try:
            if 'video' in mimetypes.guess_type(filename)[0]:
                return True
        except TypeError:
            pass
        return False

    def convert_main(self, filename):
        basename = filename.rpartition('.')[0]
        ext = filename.rpartition('.')[-1]

        if ext == 'mkv':
            return

        if ext == 'iso' and self.__inc_iso:
            # TODO - test iso conversion
            input('Important, not tested but should work\n')

            utils.run_cmd(f'extract {filename}')

            if not Path.exists(Path('VIDEO_TS')):
                print(f'missing VIDEO_TS iso dir from: {filename}')
                return
            os.chdir('VIDEO_TS')

            # TODO - convert to native python
            utils.run_cmd(f'rm -- *BUP *IFO')
            utils.run_cmd(f'find . -maxdepth 1 -type f -size +0k -size -5M -exec rm -- "{{}}" \\;')

            for v in Path(Path.cwd()).iterdir():
                iso_basename = str(v).rpartition('.')[0]
                utils.run_cmd(f'ffmpeg -hide_banner -i "{v}" '
                              f'-c:a copy -c:v copy -c:s copy "{self.__tmpdir}/{basename}-{iso_basename}.mkv"')

            os.chdir('..')
            utils.run_cmd(f'mv -- "{self.__tmpdir}/{basename}.mkv" "{Path.cwd()}"')
            utils.run_cmd(f'rm -rf -- ./AUDIO_TS ./VIDEO_TS')

            return
        else:
            if not self.check_if_video(filename=filename):
                return

            original = Path.cwd() / 'original'
            original.mkdir(parents=True, exist_ok=True)

            utils.run_cmd(f'ffmpeg -hide_banner -i "{filename}" '
                          f'-c:a copy -c:v copy -c:s copy "{self.__tmpdir}/{basename}.mkv"')

            # Path.rename does not like crossing partitions
            utils.run_cmd(f'mv -- "{self.__tmpdir}/{basename}.mkv" "{Path.cwd()}"')
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
        if args.iso:
            self.__inc_iso = True
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
    parser.add_argument('-i', '--iso',
                        action='store_true',
                        help='')
    args = parser.parse_args()

    run = Convert()
    run.run(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
