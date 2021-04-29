# -*- coding: utf-8 -*-
# 2.7.0
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

import argparse
from pathlib import Path

from python.utils.check_env import CheckEnv
from python.utils.execute import Execute
from python.utils.get_files import GetOnlyFiles
from python.utils.output_dir import OutputDir


class Compress:
    def __init__(self, args: argparse = None):
        self.__decrypt = False

        self.__output_dir = Path.cwd()

        self.__user = None

        self.run(args=args)

    def compress(self, filename):
        if self.__decrypt:
            basename = str(filename).rpartition('.')[0]
            print(f'Decrypting : {filename}')
            Execute(f'nice -19 gpg --output "{basename}" --decrypt "{filename}"')
        else:
            print(f'Encrypting : {filename}')
            Execute(f'nice -19 gpg --yes --batch -e -r "{self.__user}" "{filename}"')

    def run(self, args):
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

        GetOnlyFiles(function=self.compress, input_files=args.input_files, only_files=args.files)


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
    args = parser.parse_args()

    CheckEnv.args_required_else_help()

    Compress(args=args)
