#!/usr/bin/env python3
# 1.3.1
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

import argparse
from pathlib import Path

from utils import utils


class Compress:
    def __init__(self):
        self.__decrypt = False

        self.__input_files = None
        self.__output_dir = Path.cwd()

        self.__user = None

        self.__files = False

    def get_files(self):
        if self.__files:
            dir_listing = []
            for f in Path(Path.cwd()).iterdir():
                dir_listing.append(f)

            for f in dir_listing:
                if Path.is_file(f):
                    self.compress(filename=f)
        elif self.__input_files is not None:
            for f in self.__input_files:
                f = Path(f)
                if Path.is_file(f):
                    self.compress(filename=f)

    def compress(self, filename):
        if self.__decrypt:
            basename = str(filename).rpartition('.')[0]
            print(f'Decrypting : {filename}')
            utils.run_cmd(f'nice -19 gpg --output "{basename}" --decrypt "{filename}"')
        else:
            print(f'Encrypting : {filename}')
            utils.run_cmd(f'nice -19 gpg --yes --batch -e -r "{self.__user}" "{filename}"')

    def run(self, args):
        # compression type
        if args.files:
            self.__files = True
        if args.decrypt_dir:
            self.__files = True
            self.__decrypt = True
        if args.user:
            self.__user = args.user
        # general
        if args.list_keys:
            utils.run_cmd('gpg --list-secret-keys --keyid-format LONG')
            raise SystemExit
        # other
        if args.input_files is not None:
            self.__input_files = args.input_files
        if args.output_dir:
            out = Path.resolve(Path(args.output_dir[0]))
            if not Path.is_dir(out):
                if Path.exists(out):
                    print(f'selected output dir \'{out}\' exists but is not a directory')
                    raise SystemExit(1)
                Path(out).mkdir(parents=True, exist_ok=True)
            self.__output_dir = out

            # TODO
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
    parser.add_argument('-o', '--output-dir',
                        metavar='DIR',
                        type=list,
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

    utils.args_required_else_help()

    run = Compress()
    run.run(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
