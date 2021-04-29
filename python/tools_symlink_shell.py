#!/usr/bin/env python3
# 1.2.0
# 2021-04-29

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


class Symlink:
    def __init__(self):
        self.__bin = Path.home() / '.bin'
        self.__bin_sh = Path.home() / '.bin/shell'

        self.run()

    def symlink_main(self):
        os.chdir(self.__bin_sh)
        for f in Path(Path.cwd()).iterdir():
            if Path.is_dir(f):
                continue

            os.chdir(self.__bin)

            # remove .sh, do not use .strip('.sh)
            symlink = Path(f.name[:-3])
            real_path = Path() / 'shell' / f.name

            if Path.is_symlink(symlink):
                continue

            os.symlink(real_path, symlink)

    def run(self):
        self.symlink_main()


def main():
    Symlink()
