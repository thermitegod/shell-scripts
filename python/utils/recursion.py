# -*- coding: utf-8 -*-
# 2.4.0
# 2020-01-13

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

import os
from pathlib import Path
from typing import Callable


class RecursiveFindFiles:
    def __init__(self, path: Path = None, inc_dirs: bool = False, use_pathlib: bool = False):
        """
        :param path:
            will recursively find all files in this path, if None will use CWD
        :param use_pathlib:
            use path objects in returned list, otherwise will be str
        """

        super().__init__()

        self.__file_list_str = []
        self.__file_list_pathlib = []
        self.__use_path_obj = use_pathlib
        self.__inc_dirs = inc_dirs

        if path is not None:
            os.chdir(path)

        self._recursive_find_files()

    def _recursive_find_files(self):
        """
        gets a list of all files in every sub dir
        """

        for f in Path.cwd().iterdir():
            if f.is_file():
                self.__file_list_str.append(str(f))
                self.__file_list_pathlib.append(f)
            elif f.is_dir():
                if self.__inc_dirs:
                    self.__file_list_str.append(str(f))
                    self.__file_list_pathlib.append(f)

                os.chdir(f)
                self._recursive_find_files()

    def get_files(self):
        if self.__use_path_obj:
            return self.__file_list_pathlib
        else:
            return self.__file_list_str


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
