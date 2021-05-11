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


class Compress:
    def __init__(self, args: argparse = None):
        self.__output_dir = Path.cwd()

        self.__input_files = None
        self.__directories = False
        self.__files = False

        self.__exclude = ''
        self.__compression_method = None

        self.__run_tests = True
        self.__file_list = []

        self.__junk_paths = '--junk-paths'

        self.__destructive = False

        self.parse_args(args=args)

        GetFiles(function=self.compress, input_files=self.__input_files,
                 only_directories=self.__directories, only_files=self.__files)

        self.run_tests()

    def run_tests(self):
        if self.__run_tests:
            for f in self.__file_list:
                Execute(f'mk7z -T "{f}"')

    def compress(self, filename, compressing_dir):
        basename = Path(filename).name
        output_file = Path() / self.__output_dir / f'{basename}.zip'
        if Path.exists(output_file):
            print(f'Skipping, archive already exists at: \'{output_file}\'')
            return

        self.__file_list.append(f'{self.__output_dir}/{basename}.zip')

        RemoveJunk(Path(filename))

        os.chdir(Path(filename).parent)

        Execute(f'nice -19 zip {self.__exclude} -rv -9 '
                f'--compression-method={self.__compression_method} '
                f'{self.__junk_paths} "{output_file}" "{basename}"')

        if Path.exists(output_file):
            if self.__destructive:
                if compressing_dir:
                    shutil.rmtree(filename)
                else:
                    Path.unlink(Path(filename))
        else:
            print(f'ERROR: archive not created for: \'{filename}\'')
            raise SystemExit(1)

    def parse_args(self, args):
        # destructive
        if args.no_junk_paths:
            self.__junk_paths = ''
        if args.destructive:
            self.__destructive = True
        # other
        if args.compression_method:
            self.__compression_method = args.compression_method[0]
        if args.disable_tests:
            self.__run_tests = False
        if args.output_dir:
            self.__output_dir = OutputDir(directory=args.output_dir).get_dir()
        if args.exclude:
            for e in args.exclude:
                self.__exclude += f'--exclude="{e}" '

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
                        type=list,
                        nargs='*',
                        help='exclude files from archive')
    parser.add_argument('-P', '--disable-tests',
                        action='store_true',
                        help='disable post compression test')
    parser.add_argument('-o', '--output-dir',
                        metavar='DIR',
                        nargs=1,
                        help='create the archive[s] in this directory')
    batch = parser.add_argument_group('compression')
    batch.add_argument('-cm', '--compression-method',
                       default=['deflate'],
                       nargs=1,
                       metavar='CM',
                       choices=['store', 'deflate', 'bzip2'],
                       help='set zip compression method, [store, defalte, bzip2]')
    batch = parser.add_argument_group('batch creation')
    batch.add_argument('-d', '--directories',
                       action='store_true',
                       help='compress all directories in cwd')
    batch.add_argument('-f', '--files',
                       action='store_true',
                       help='compress all files in cwd')
    rm = parser.add_argument_group('destructive')
    rm.add_argument('-j', '--no-junk-paths',
                    action='store_true',
                    help='do not run zip with \'--junk-paths\'')
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
