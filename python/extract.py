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
# 2.9.0
# 2021-04-29


# TODO
#   dynamically decide whether to have self.__extract_to_subdir set to True or False

import argparse
import os
import sys
from pathlib import Path

from loguru import logger

from utils.check_env import CheckEnv
from utils.execute import Execute
from utils.get_files import GetOnlyFiles
from utils.output_dir import OutputDir


class Decompress:
    def __init__(self, args: argparse = None):
        self.__output_dir = None

        self.__input_files = None
        self.__files = False

        self.__extract_to = False
        self.__extract_to_subdir = True

        self.parse_args(args=args)

        GetOnlyFiles(function=self.run_extraction, input_files=self.__input_files, only_files=self.__files)

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
            Execute(f'tar -xvjf "{filename_path}"')

        elif filename.endswith(('.tar.gz', '.tgz')):
            Execute(f'tar -xvzf "{filename_path}"')

        elif filename.endswith(('.tar.xz', '.txz')):
            Execute(f'tar -xvJf "{filename_path}"')

        elif filename.endswith('.tar.zst'):
            Execute(f'zstd -dc --long=31 \'{filename_path}\' | tar xvf -', sh_wrap=True)

        elif filename.endswith('.tar.lz4'):
            Execute(f'lz4 -dc \'{filename_path}\' | tar xvf -', sh_wrap=True)

        elif filename.endswith('.tar.lzma'):
            Execute(f'tarlzma -xvf "{filename_path}"')

        elif filename.endswith('.tar.lrz'):
            Execute(f'lrzuntar "{filename_path}"')

        elif filename.endswith(('.rar', '.RAR', '.cbr')):
            Execute(f'unrar "{filename_path}"')

        elif filename.endswith('.gz'):
            Execute(f'gunzip -k "{filename_path}"')

        elif filename.endswith('.xz'):
            Execute(f'unxz -k "{filename_path}"')

        elif filename.endswith('.bz2'):
            Execute(f'bzip2 -dk "{filename_path}"')

        elif filename.endswith('.zst'):
            Execute(f'unzstd -d --long=31 "{filename_path}"')

        elif filename.endswith('.tar'):
            Execute(f'tar -xvf "{filename_path}"')

        elif filename.endswith(('.zip', '.cbz')):
            Execute(f'unzip "{filename_path}"')

        elif filename.endswith(('.7z', '.iso', '.ISO')):
            Execute(f'7z x "{filename_path}"')

        else:
            print(f'cannot extract: \'{filename_path}\'')

    def parse_args(self, args):
        # decompression type
        if args.no_subdir:
            self.__extract_to_subdir = False
        # other
        if args.output_dir:
            self.__extract_to = True
            self.__output_dir = OutputDir(directory=args.output_dir).get_dir()

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
                        help='decompress all files in cwd')
    parser.add_argument('-o', '--output-dir',
                        metavar='DIR',
                        nargs=1,
                        help='create the archive[s] in this directory')
    opts = parser.add_argument_group('extraction options')
    opts.add_argument('-s', '--no-subdir',
                      action='store_true',
                      help='Extract files to output dir without creating sub directories, req -o')
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

    CheckEnv.args_required_else_help()

    Decompress(args=args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
