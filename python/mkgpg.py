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
# 2.8.0
# 2021-04-29


import argparse
import sys
from pathlib import Path

from loguru import logger

from utils.check_env import CheckEnv
from utils.execute import Execute
from utils.get_files import GetOnlyFiles
from utils.output_dir import OutputDir


class Compress:
    def __init__(self, args: argparse = None):
        self.__decrypt = False

        self.__output_dir = Path.cwd()

        self.__user = None

        self.__input_files = None
        self.__files = False

        self.parse_args(args=args)

        GetOnlyFiles(function=self.compress, input_files=self.__input_files, only_files=self.__files)

    def compress(self, filename):
        if self.__decrypt:
            basename = str(filename).rpartition('.')[0]
            print(f'Decrypting : {filename}')
            Execute(f'nice -19 gpg --output "{basename}" --decrypt "{filename}"')
        else:
            print(f'Encrypting : {filename}')
            Execute(f'nice -19 gpg --yes --batch -e -r "{self.__user}" "{filename}"')

    def parse_args(self, args):
        # compression type
        if args.decrypt_dir:
            self.__decrypt = True
        if args.user:
            self.__user = args.user
        # general
        if args.list_keys:
            Execute('gpg --list-secret-keys --keyid-format LONG')
            raise SystemExit
        # other
        if args.output_dir:
            self.__output_dir = OutputDir(directory=args.output_dir).get_dir()

            # TODO
            raise NotImplementedError

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
    parser.add_argument('-o', '--output-dir',
                        metavar='DIR',
                        nargs=1,
                        help='create the gpg files in this directory')
    parser.add_argument('-d', '--decrypt-dir',
                        action='store_true',
                        help='decrypt all gpg files in cwd')
    parser.add_argument('-f', '--files',
                        action='store_true',
                        help='gpg all files in cwd')
    parser.add_argument('-l', '--list-keys',
                        action='store_true',
                        help='print available keys')
    parser.add_argument('-u', '--user',
                        metavar='USER',
                        nargs=1,
                        default='brandon',
                        help='User to use')
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


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
