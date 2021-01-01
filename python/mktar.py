# -*- coding: utf-8 -*-
# 2.7.0
# 2021-01-01

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

# changes should be disseminated to the following scripts when applicable
# mktar
# mkzst
# mkzip
# mk7z
# these are based on each other but different enough that they
# are separated into unique scripts

import argparse
import os
import shutil
from pathlib import Path

from python.utils.check_env import CheckEnv
from python.utils.execute import Execute
from python.utils.get_files import GetFiles
from python.utils.output_dir import OutputDir


class Compress:
    def __init__(self):
        self.__output_dir = Path.cwd()

        self.__exclude = ''

        self.__junk_paths = False

        self.__tar_verbose = ''

        self.__destructive = False

    def compress(self, filename, compressing_dir):
        test_file = Path() / self.__output_dir / f'{filename}.tar'
        if Path.exists(test_file):
            print(f'Skipping, archive already exists at: \'{test_file}\'')
            return

        os.chdir(Path(filename).parent)
        file_name = Path(filename).name

        if self.__junk_paths:
            # simulates zip --junk-path

            # Notes: archives all files in 'file' and creates archive
            # without a basedir. i.e. creates archive of only files
            # but if nested dirs exist then they still get created

            file_list = []
            for f in Path(file_name).iterdir():
                file_list.append(str(f.name))
                if f.is_dir():
                    print(f'SUBDIR will be created in archive: {f}')

            file_list_comp = ''
            for f in file_list:
                file_list_comp += f'"{f}" '

            cmd = f'tar {self.__exclude} --directory="{filename.resolve()}" -{self.__tar_verbose}Scf ' \
                  f'"{self.__output_dir}/{file_name}.tar" {file_list_comp}'
        else:
            cmd = f'tar {self.__exclude} --xattrs -{self.__tar_verbose}Scf ' \
                  f'"{self.__output_dir}/{file_name}.tar" "{file_name}"'

        Execute(cmd)

        if Path.exists(test_file):
            if self.__destructive:
                if compressing_dir:
                    shutil.rmtree(filename)
                else:
                    Path.unlink(filename)
        else:
            print(f'ERROR: archive not created for: \'{filename}\'')
            raise SystemExit(1)

    def run(self, args):
        # destructive
        if args.destructive:
            self.__destructive = True
        # other
        if args.output_dir:
            self.__output_dir = OutputDir(directory=args.output_dir).get_dir()
        if args.verbose:
            self.__tar_verbose = 'v'
        if args.exclude:
            for e in args.exclude:
                self.__exclude += f'--exclude="{e}" '
        if args.junk_paths:
            self.__junk_paths = True

        GetFiles(function=self.compress, input_files=args.input_files,
                 only_directories=args.directories, only_files=args.files)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_files',
                        action='store',
                        type=str,
                        nargs='*',
                        default=None,
                        help=argparse.SUPPRESS)
    parser.add_argument('-e', '--exclude',
                        metavar='EX',
                        nargs='*',
                        help='exclude files from archive')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='enable verbose tar')
    parser.add_argument('-j', '--junk-paths',
                        action='store_true',
                        help='simulates \'zip --junk-paths\'')
    parser.add_argument('-o', '--output-dir',
                        metavar='DIR',
                        type=list,
                        nargs=1,
                        help='create the archive[s] in this directory')
    batch = parser.add_argument_group('batch creation')
    batch.add_argument('-d', '--directories',
                       action='store_true',
                       help='compress all directories in cwd')
    batch.add_argument('-f', '--files',
                       action='store_true',
                       help='compress all files in cwd')
    rm = parser.add_argument_group('destructive')
    rm.add_argument('-z', '--destructive',
                    action='store_true',
                    help='Delete original after it is compressed')
    args = parser.parse_args()

    CheckEnv.args_required_else_help()

    run = Compress()
    run.run(args)
