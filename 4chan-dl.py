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

import argparse
import os
from pathlib import Path

from utils import utils
from utils import dirs


class Dl:
    def __init__(self):
        self.__batch = False
        self.__input = None

        self.__board = None
        self.__thread = None
        self.__save_dir = None

        self.__url = None
        self.__save_dir_full = None

        script_name = utils.get_script_name()
        if script_name == '4chan-dl':
            self.__thread_list = Path() / dirs.get_extra_dir() / script_name
            self.__dir = Path() / dirs.get_download_dir() / 'chan/4chan'
            self.__url_base = 'https://boards.4chan.org'
        elif script_name == '8chan-dl':
            self.__thread_list = Path() / dirs.get_extra_dir() / script_name
            self.__dir = Path() / dirs.get_download_dir() / 'chan/8chan'
            self.__url_base = 'https://8kun.top/'

            # TODO
            raise NotImplementedError

    def dl(self):
        utils.run_cmd(f'chandl -d {self.__save_dir_full} -t {os.cpu_count()} -url "{self.__url}"')

    def dl_batch(self):
        self.__url = f'{self.__url_base}/{self.__board}/thread/{self.__thread}'
        self.__save_dir_full = Path() / self.__dir / self.__board / self.__save_dir
        self.dl()

    def main(self):
        if not self.__batch:
            try:
                self.__save_dir_full = self.__input[0]
                self.__url = self.__input[1]
                self.dl()
                raise SystemExit
            except IndexError:
                print(f'Example: {utils.get_script_name()} <save dir> <link>')
                raise SystemExit

        for line in Path.open(self.__thread_list):
            line = line.strip('\n').split(' ')
            if line[0].startswith('#'):
                continue

            # set config file variables
            try:
                self.__board = line[0]
                self.__thread = line[1]
                self.__save_dir = line[2]
            except IndexError:
                # skip line if malformed
                continue

            self.dl_batch()

    def run(self, args):
        if args.input_files is not None:
            self.__input = args.input_files
        if args.batch:
            self.__batch = True
        if args.edit:
            utils.edit_conf(self.__thread_list)

        self.main()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_files',
                        action='store',
                        type=str,
                        nargs='*',
                        default=None,
                        help=argparse.SUPPRESS)
    parser.add_argument('-b', '--batch',
                        action='store_true',
                        help='run batch file')
    parser.add_argument('-e', '--edit',
                        action='store_true',
                        help='edit batch file')
    args = parser.parse_args()

    utils.args_required_else_help()

    run = Dl()
    run.run(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
