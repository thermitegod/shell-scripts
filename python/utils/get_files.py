# Copyright (C) 2018-2022 Brandon Zorn <brandonzorn@cock.li>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# SCRIPT INFO
# 2.1.0
# 2020-11-13


from pathlib import Path

from typing import Callable


class GetFiles:
    def __init__(self, function: Callable, input_files: list = None,
                 only_directories: bool = False, only_files: bool = False):
        """
        Can be run for all directories, all files, all directories and files, or
        a list of files

        :param function:
            callback function, function(filename, compressing_dir)
        :param input_files:
            list of files to run on
        :param only_directories:
            only run on directories ignoring files
        :param only_files:
            only run on files ignoring directories
        :return:
        """

        super().__init__()

        if only_directories or only_files:
            dir_listing: list[Path] = []
            for f in Path(Path.cwd()).iterdir():
                dir_listing.append(f)

            for f in dir_listing:
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


class GetOnlyFiles:
    def __init__(self, function: Callable, input_files: list = None,
                 only_files: bool = False):
        """
        Can be run for all files, or a list of files

        :param function:
            callback function, function(filename)
        :param input_files:
            list of files to run on
        :param only_files:
            only run on files ignoring directories
        :return:
        """

        super().__init__()

        if only_files:
            dir_listing: list[Path] = []
            for f in Path(Path.cwd()).iterdir():
                dir_listing.append(f)

            for f in dir_listing:
                if Path.is_file(f):
                    function(filename=f)

        elif input_files is not None:
            for f in input_files:
                f = Path(f).resolve()
                if Path.is_file(f):
                    function(filename=f)
