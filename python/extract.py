#!/usr/bin/env python3
# 1.7.1
# 2020-10-08

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

from utils import utils


class Decompress:
    def __init__(self):
        self.__input_files = None

        self.__output_dir = None

        self.__files = False

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

    def get_files(self):
        if self.__files:
            dir_listing = []
            for f in Path(Path.cwd()).iterdir():
                dir_listing.append(str(f))

            for f in dir_listing:
                if Path.is_file(Path(f)) and self.__files:
                    self.run_extraction(filename=f)
        elif self.__input_files is not None:
            for f in self.__input_files:
                f = str(Path(f).resolve())
                if Path.is_file(Path(f)):
                    self.run_extraction(filename=f)

    def run(self, args):
        # decompression type
        if args.files:
            self.__files = True
        if args.no_subdir:
            self.__extract_to_subdir = False
        # other
        if args.input_files is not None:
            self.__input_files = args.input_files
        if args.output_dir:
            self.__extract_to = True
            out = Path.resolve(Path(args.output_dir[0]))
            if not Path.is_dir(out):
                if Path.exists(out):
                    print(f'selected output dir \'{out}\' exists but is not a directory')
                    raise SystemExit(1)
                out.mkdir(parents=True, exist_ok=True)
            self.__output_dir = out

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
                        help='decompress all files in cwd')
    parser.add_argument('-o', '--output-dir',
                        metavar='DIR',
                        type=list,
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