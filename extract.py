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

# TODO
#   output dir for all compressors
#   implement subdirectory extraction

# Notes
#   taken from mkzst
#       args.output_dir
#       get_files()

import argparse
from pathlib import Path

from utils import utils


class Decompress:
    def __init__(self):
        self.__cmd = None
        self.__input_files = None
        self.__output_dir = None
        self.__files = False
        self.__supported = True
        self.__subdir_extract = False

    def run_extraction(self, filename: str):
        filename = str(filename)
        if filename.endswith('.tar.bz2'):
            self.__cmd = f'tar xvjf -- "{filename}"'
        elif filename.endswith('.tar.gz'):
            self.__cmd = f'tar xvzf -- "{filename}"'
        elif filename.endswith('.tar.xz'):
            self.__cmd = f'tar xvJf -- "{filename}"'
        elif filename.endswith('.tar.zst'):
            # runs in sh wrapper because of pipes
            self.__cmd = f'sh -c "zstd -dc --long=31 -- "{filename}" | tar xvf -"'
        elif filename.endswith('.tar.lz4'):
            # runs in sh wrapper because of pipes
            self.__cmd = f'sh -c "lz4 -dc -- "{filename}" | tar xvf -"'
        elif filename.endswith('.tar.lzma'):
            self.__cmd = f'tarlzma xvf -- "{filename}"'
        elif filename.endswith('.tar.lrz'):
            self.__cmd = f'lrzuntar -- "{filename}"'
        elif filename.endswith('.rar') or filename.endswith('RAR'):
            self.__cmd = f'unrar -- "{filename}"'
        elif filename.endswith('.gz'):
            self.__cmd = f'gunzip -k -- "{filename}"'
        elif filename.endswith('.xz'):
            self.__cmd = f'unxz -k -- "{filename}"'
        elif filename.endswith('.bz2'):
            self.__cmd = f'bzip2 -dk -- "{filename}"'
        elif filename.endswith('.zst'):
            self.__cmd = f'unzstd -d --long=31 -- "{filename}"'
        elif filename.endswith('.tgz') or filename.endswith('.tbz2'):
            self.__cmd = f'tar xvf -- "{filename}"'
        elif filename.endswith('.txz'):
            self.__cmd = f'tar xvJf -- "{filename}"'
        elif filename.endswith('.tar'):
            self.__cmd = f'tar xvf -- "{filename}"'
        elif filename.endswith('.zip'):
            self.__cmd = f'unzip -- "{filename}"'
        elif filename.endswith('.7z'):
            self.__cmd = f'7z x -- "{filename}"'
        elif filename.endswith('iso') or filename.endswith('ISO'):
            # TODO
            if self.__subdir_extract:
                pass
            self.__cmd = f'7z x -- "{filename}"'
        elif filename.endswith('.cbz'):
            # TODO
            if self.__subdir_extract:
                pass
            self.__cmd = f'7z x -- "{filename}"'
        elif filename.endswith('.cbr'):
            # TODO
            if self.__subdir_extract:
                pass
            self.__cmd = f'unrar -- "{filename}"'
        else:
            print(f'cannot extract: \'{filename}\'')
            self.__supported = False

        if self.__supported:
            utils.run_cmd(self.__cmd)
        else:
            self.__supported = True

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
                if Path.is_file(Path(f)):
                    self.run_extraction(filename=f)

    def run(self, args):
        # decompression type
        if args.files:
            self.__files = True
        if args.subdir:
            self.__subdir_extract = True
        # other
        if args.input_files is not None:
            self.__input_files = args.input_files
        if args.output_dir:
            out = Path.resolve(Path(args.output_dir))
            if not Path.is_dir(out):
                if Path.exists(out):
                    utils.die(msg=f'selected output dir \'{out}\' exists but is not a directory')
                Path(out).mkdir(parents=True, exist_ok=True)
            self.__output_dir = out

            # TODO
            #   need to plumb into decompressors
            raise NotImplementedError

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
                        help='create the archive[s] in this directory')
    opts = parser.add_argument_group('EXTRACTION OPTIONS')
    opts.add_argument('-s', '--subdir',
                      action='store_true',
                      help='Extract archive to a directory created from filename, only cb{r,z} and iso')

    args = parser.parse_args()

    utils.args_required_else_help()

    run = Decompress()
    run.run(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
