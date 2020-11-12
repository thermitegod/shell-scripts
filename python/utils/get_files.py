# -*- coding: utf-8 -*-
# 1.1.0
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

from pathlib import Path

from typing import Callable


class _GetFiles:
    def __init__(self):
        self.__dir_listing = []

    def get_files(self, function: Callable, input_files: list = None,
                  only_directories: bool = False, only_files: bool = False):
        """
        :param function:
        :param input_files:
        :param only_directories:
        :param only_files:
        :return:
        """

        if only_directories or only_files:
            self.__dir_listing = []
            for f in Path(Path.cwd()).iterdir():
                self.__dir_listing.append(f)

            for f in self.__dir_listing:
                if Path.is_dir(f) and only_directories:
                    function(filename=f, compressing_dir=True)
                elif Path.is_file(f) and only_files:
                    function(filename=f, compressing_dir=False)

        elif input_files is not None:
            for f in input_files:
                f = Path(f).resolve()
                if Path.is_dir(f):
                    function(filename=f, compressing_dir=True)
                elif Path.is_file(f):
                    function(filename=f, compressing_dir=False)

        else:
            pass

    def get_only_files(self, function: Callable, input_files: list = None, only_files: bool = False):
        """
        :param function:
        :param input_files:
        :param only_files:
        :return:
        """

        if only_files:
            self.__dir_listing = []
            for f in Path(Path.cwd()).iterdir():
                self.__dir_listing.append(f)

            for f in self.__dir_listing:
                if Path.is_file(f) and only_files:
                    function(filename=f)

        elif input_files is not None:
            for f in input_files:
                f = Path(f).resolve()
                if Path.is_file(f):
                    function(filename=f)


GetFiles = _GetFiles()
