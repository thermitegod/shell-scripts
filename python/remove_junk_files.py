# -*- coding: utf-8 -*-
# 1.0.0
# 2021-01-13

# Copyright (C) 2021 Brandon Zorn <brandonzorn@cock.li>
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
import shutil
from collections import namedtuple

from python.utils.recursion import RecursiveFindFiles


class RemoveJunk:
    def __init__(self):

        Junk = namedtuple('Junk', ['name', 'is_dir'])

        self.__junk = (
            Junk('desktop.ini', False),
            Junk('Thumbs.db', False),
            Junk('.DS_Store', False),
            Junk('__MACOSX', True),

            # Junk('', True),
            # Junk('', True),
            # Junk('', True),
        )

        self.__file_list_done = []
        self.__file_list_only = []
        self.__file_list = []

    def main(self, list_only: bool = False):
        self.__file_list = RecursiveFindFiles(inc_dirs=True, use_pathlib=True).get_files()

        for junk in self.__junk:
            if len(self.__file_list) == 0:
                break

            for idx, item in enumerate(self.__file_list):
                if item.name == junk.name:
                    if list_only:
                        self.__file_list_done.append(item)
                        self.__file_list_only.append(item)
                    else:
                        self.__file_list_done.append(item)
                        if junk.is_dir:
                            shutil.rmtree(item)
                        else:
                            item.unlink()

            for idx, item in enumerate(self.__file_list_done):
                self.__file_list.remove(item)
            self.__file_list_done = []

            if self.__file_list_only:
                print(f'Found {junk.name}')
                print(f'==========================')
                for f in self.__file_list_only:
                    print(f)
                print('\n')
                self.__file_list_only = []

    def run(self, args):
        if args.list:
            self.main(list_only=True)
        else:
            self.main()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list',
                        action='store_true',
                        help='List files that match patern')
    args = parser.parse_args()

    run = RemoveJunk()
    run.run(args)
