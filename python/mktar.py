# -*- coding: utf-8 -*-
# 2.12.0
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
import sys
from pathlib import Path

from loguru import logger

from python.utils.archive_utils import RemoveJunk
from python.utils.check_env import CheckEnv
from python.utils.execute import Execute
from python.utils.get_files import GetFiles
from python.utils.output_dir import OutputDir
from python.utils.recursion import RecursiveFindFiles


class Compress:
    def __init__(self, args: argparse = None):
        self.__output_dir = Path.cwd()

        self.__input_files = None
        self.__directories = False
        self.__files = False

        self.__exclude = ''

        self.__junk_paths = False

        self.__tar_verbose = ''

        self.__destructive = False

        self.parse_args(args=args)

        GetFiles(function=self.compress, input_files=self.__input_files,
                 only_directories=self.__directories, only_files=self.__files)

    def compress(self, filename, compressing_dir):
        test_file = Path() / self.__output_dir / f'{filename}.tar'
        if Path.exists(test_file):
            print(f'Skipping, archive already exists at: \'{test_file}\'')
            return

        RemoveJunk(Path(filename))

        os.chdir(Path(filename).parent)
        file_name = Path(filename).name

        if self.__junk_paths:
            # simulates zip --junk-path

            # Notes: archives all files in 'file' and creates archive
            # without a basedir. i.e. creates archive of only files
            # without a directory structure

            if Path.is_file(filename):
                print(f'ERROR: --junk-paths only works for directories')
                return

            file_list = RecursiveFindFiles(path=Path(filename)).get_files()

            file_list_comp = ''
            for f in file_list:
                # .partition() prevents tar error messages by removing
                # leading '/'. the entire path will be junked anyway so
                # its fine
                # tar: Removing leading `/' from member names
                # tar: Removing leading `/' from hard link targets
                file_list_comp += f'"{f.partition("/")[-1]}" '

            # https://stackoverflow.com/questions/4898056/how-to-create-flat-tar-archive
            # --transform 's/.*\///g'
            remove_dir_structure = '--transform \'s/.*\\///g\''

            cmd = f'tar {self.__exclude} --directory="{filename.resolve()}" --sort=name -{self.__tar_verbose}cf ' \
                  f'"{self.__output_dir}/{file_name}.tar" {remove_dir_structure} -C / {file_list_comp}'
        else:
            cmd = f'tar {self.__exclude} --xattrs -{self.__tar_verbose}cf ' \
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

    def parse_args(self, args):
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

        self.__input_files = args.input_files
        self.__files = args.files
        self.__directories = args.directories


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

    Compress(args=args)
