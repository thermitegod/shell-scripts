# -*- coding: utf-8 -*-
# 1.0.0
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

import os
from pathlib import Path
from typing import Callable


class _Recursion:
    def __init__(self):
        self.__file_list = []
        pass

    def recursive_find(self, function: Callable):
        for f in Path(Path.cwd()).iterdir():
            if f.is_dir():
                os.chdir(f)
                function()
                self.recursive_find(function=function)

    def recursive_find_files(self):
        for f in Path(Path.cwd()).iterdir():
            if f.is_file():
                self.__file_list.append(str(f))
            elif f.is_dir():
                os.chdir(f)
                self.recursive_find_files()

        return self.__file_list


Recursion = _Recursion()
