# -*- coding: utf-8 -*-
# 3.0.0
# 2021-06-09

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
from multiprocessing.dummy import Pool as ThreadPool
from pathlib import Path
from typing import Callable


class RecursiveFindFiles:
    def __init__(self, path: Path = None, inc_dirs: bool = False):
        """
        :param path:
            will recursively find all files in this path, if None will use CWD
        :param inc_dirs:
            include directories otherwise only include files
        """

        super().__init__()

        self.__file_list_str = []
        self.__file_list_pathlib = []
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

    def get_files(self, pathlib: bool = False):
        """
        :param pathlib:
            use path objects in returned list, otherwise will be str
        :return:
            list of files
        """

        if pathlib:
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


class RecursiveExecuteThreadpool:
    def __init__(self, function: Callable):
        """
        :param function:
            run this function in each sub dir,
            function must take a Path arg and
            should use abs paths for everything
            without using os.chdir, otherwise you're
            going to have a bad time
        """

        super().__init__()

        # limit total number
        threadpool = ThreadPool(os.cpu_count() // 4)

        # dir_list = [d for d in Path(Path.cwd()).iterdir() if d.is_dir()]
        dir_list = [d for d in Path.cwd().rglob("*") if d.is_dir()]

        threadpool.map(function, dir_list)
        threadpool.close()
        threadpool.join()
