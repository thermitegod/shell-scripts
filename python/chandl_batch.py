# -*- coding: utf-8 -*-
# 2.4.0
# 2021-04-29

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

# wrapper script around chandl to batch download threads

import os
from pathlib import Path

from python.utils import dirs
from python.utils.execute import Execute

try:
    from python.private.thread_list import ThreadList
except ImportError:
    print('Missing config file, see python/template/thread_list.py')
    raise SystemExit(1)


class Dl:
    def __init__(self):
        self.__board = None
        self.__thread = None
        self.__save_dir = None

        self.__url = None
        self.__save_dir_full = None

        # script_name = CheckEnv.get_script_name()
        # if script_name == '4chan-dl':
        self.__thread_list = ThreadList.THREADS_4CHAN
        self.__dir = Path() / dirs.get_download_dir() / 'chan/4chan'
        self.__url_base = 'https://boards.4chan.org'
        # elif script_name == '8chan-dl':
        #     self.__thread_list = ThreadList.THREADS_8KUN
        #     self.__dir = Path() / dirs.get_download_dir() / 'chan/8chan'
        #     self.__url_base = 'https://8kun.top/'

        self.main()

    def dl(self):
        Execute(f'chandl -d {self.__save_dir_full} -t {os.cpu_count()} -url "{self.__url}"')

    def dl_batch(self):
        self.__url = f'{self.__url_base}/{self.__board}/thread/{self.__thread}'
        self.__save_dir_full = Path() / self.__dir / self.__board / self.__save_dir
        self.dl()

    def main(self):
        for c in self.__thread_list:
            self.__board = c.board
            self.__thread = c.thread_number
            self.__save_dir = c.save_dir

            self.dl_batch()


def main():
    Dl()
