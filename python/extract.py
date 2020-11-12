#!/usr/bin/env python3
# 2.1.0
# 2020-11-11

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

# TODO
#   dynamically decide whether to have self.__extract_to_subdir set to True or False

import argparse
import os
from pathlib import Path

from utils import output_dir
from utils import utils
from utils.get_files import GetFiles


class Decompress:
    def __init__(self):
        self.__output_dir = None

        self.__extract_to = False
        self.__extract_to_subdir = True

    def extract_to(self, filename):
        if self.__extract_to_subdir:
            if '.tar.' in filename:
                # removes both extensions
                basename = filename.split('/')[-1].rpartition('.')[0].rpartition('.')[0]
            else:
                basename = filename.split('/')[-1].rpartition('.')[0]

            extract_location = Path() / self.__output_dir / basename
        else:
            extract_location = Path() / self.__output_dir

        extract_location.mkdir(parents=True, exist_ok=True)
        os.chdir(extract_location)

    def run_extraction(self, filename: str):
        filename = str(filename)

        if self.__extract_to:
            self.extract_to(filename=filename)

        # since extract_to() will change the CWD have to use absolute path
        # when calling extraction programs
        filename_path = Path(filename).resolve()

        if filename.endswith(('.tar.bz2', '.tbz2')):
            utils.run_cmd(f'tar -xvjf "{filename_path}"')

        elif filename.endswith(('.tar.gz', '.tgz')):
            utils.run_cmd(f'tar -xvzf "{filename_path}"')

        elif filename.endswith(('.tar.xz', '.txz')):
            utils.run_cmd(f'tar -xvJf "{filename_path}"')

        elif filename.endswith('.tar.zst'):
            utils.run_cmd(f'zstd -dc --long=31 \'{filename_path}\' | tar xvf -', sh_wrap=True)

        elif filename.endswith('.tar.lz4'):
            utils.run_cmd(f'lz4 -dc \'{filename_path}\' | tar xvf -', sh_wrap=True)

        elif filename.endswith('.tar.lzma'):
            utils.run_cmd(f'tarlzma -xvf "{filename_path}"')

        elif filename.endswith('.tar.lrz'):
            utils.run_cmd(f'lrzuntar "{filename_path}"')

        elif filename.endswith(('.rar', '.RAR', '.cbr')):
            utils.run_cmd(f'unrar "{filename_path}"')

        elif filename.endswith('.gz'):
            utils.run_cmd(f'gunzip -k "{filename_path}"')

        elif filename.endswith('.xz'):
            utils.run_cmd(f'unxz -k "{filename_path}"')

        elif filename.endswith('.bz2'):
            utils.run_cmd(f'bzip2 -dk "{filename_path}"')

        elif filename.endswith('.zst'):
            utils.run_cmd(f'unzstd -d --long=31 "{filename_path}"')

        elif filename.endswith('.tar'):
            utils.run_cmd(f'tar -xvf "{filename_path}"')

        elif filename.endswith(('.zip', '.cbz')):
            utils.run_cmd(f'unzip "{filename_path}"')

        elif filename.endswith(('.7z', '.iso', '.ISO')):
            utils.run_cmd(f'7z x "{filename_path}"')

        else:
            print(f'cannot extract: \'{filename_path}\'')

    def run(self, args):
        # decompression type
        if args.no_subdir:
            self.__extract_to_subdir = False
        # other
        if args.output_dir:
            self.__extract_to = True
            self.__output_dir = output_dir.set_output_dir(directory=args.output_dir)

        GetFiles.get_only_files(function=self.run_extraction, input_files=args.input_files, only_files=args.files)


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
                        help='decompress all files in cwd')
    parser.add_argument('-o', '--output-dir',
                        metavar='DIR',
                        nargs=1,
                        help='create the archive[s] in this directory')
    opts = parser.add_argument_group('EXTRACTION OPTIONS')
    opts.add_argument('-s', '--no-subdir',
                      action='store_true',
                      help='Extract files to output dir without creating sub directories, req -o')
    args = parser.parse_args()

    utils.args_required_else_help()

    run = Decompress()
    run.run(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
