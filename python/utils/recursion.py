# -*- coding: utf-8 -*-
# 2.1.0
# 2020-12-13

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

import os
from pathlib import Path
from typing import Callable


class RecursiveFindFiles:
    def __init__(self):
        super().__init__()

        self.__file_list: list[str] = []

        self._recursive_find_files()

    def _recursive_find_files(self):
        """
        gets a list of all files in every sub dir
        """

        for f in Path(Path.cwd()).iterdir():
            if f.is_file():
                self.__file_list.append(str(f))
            elif f.is_dir():
                os.chdir(f)
                self._recursive_find_files()

    def get_files(self):
        return self.__file_list


class RecursiveExecute:
    def __init__(self, function: Callable):
        """
        :param function:
            run this function in each sub dir,
            function takes no args
        """

        super().__init__()

        for f in Path(Path.cwd()).iterdir():
            if f.is_dir():
                os.chdir(f)
                function()
                RecursiveExecute(function=function)
