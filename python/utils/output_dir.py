# -*- coding: utf-8 -*-
# 2.0.0
# 2020-11-23

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


class OutputDir:
    def __init__(self, directory: list):
        """
        takes a list, created by argparse, that should have one path and
        checks if it exists otherwise will create the directory. if the
        supplied path exists and is not a directory then exit

        :param directory:
            directory to use as output dir
        """

        super().__init__()

        self.__out = Path.resolve(Path(directory[0]))

        if not Path.is_dir(self.__out):
            if Path.exists(self.__out):
                print(f'selected output dir \'{self.__out}\' exists, but is not a directory')
                raise SystemExit(1)
            self.__out.mkdir(parents=True, exist_ok=True)

    def get_dir(self):
        """
        :return:
             returns the absolute path for the output directory
        """

        return self.__out
