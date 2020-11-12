# -*- coding: utf-8 -*-
# 1.3.0
# 2020-11-11

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

from python.utils import utils
from python.utils.recursion import Recursion


class Count:
    def __init__(self):
        self.__type_archive = ('.zip', '.7z', '.rar', '.cbr', '.cbz', '.cb7', '.tar',
                               '.bz2', '.gz', '.lz4', '.lzo', '.xz', '.zst')
        self.__type_image = ('.png', '.jpg', '.jpeg', '.jpe', '.gif', '.bmp', '.ico', )
        self.__type_video = ('.webm', '.mp4', '.mkv', '.avi', '.mov', '.wmv')

        script = utils.get_script_name()
        if script == 'count-image':
            self.__mode = self.__type_archive
        elif script == 'count-archive':
            self.__mode = self.__type_image
        elif script == 'count-video':
            self.__mode = self.__type_video
        else:
            print(f'Unknown mode: {script}')
            raise SystemExit(1)

        self.__counter = 0
        self.__counter_total = 0

        self.__file_list = []

    def main_count(self):
        self.__file_list = Recursion.recursive_find_files()

        for ext in self.__mode:
            for f in self.__file_list:
                if f.endswith(ext):
                    # TODO - get incorrect count when removing
                    # self.__file_list.remove(f)
                    self.__counter += 1

            if self.__counter != 0:
                print(f'{ext[1:].upper()}\t: {self.__counter}')
                self.__counter_total += self.__counter
                self.__counter = 0

        if self.__counter_total != 0:
            print(f'Total\t: {self.__counter_total}')

    def main_list(self):
        self.__file_list = Recursion.recursive_find_files()

        for ext in self.__mode:
            print(f'Listing all of: {ext[1:].upper()}')
            for f in self.__file_list:
                if f.endswith(ext):
                    print(f)

    def run(self, args):
        if args.list:
            self.main_list()
        else:
            self.main_count()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list',
                        action='store_true',
                        help='List files that match patern')
    args = parser.parse_args()

    run = Count()
    run.run(args)
