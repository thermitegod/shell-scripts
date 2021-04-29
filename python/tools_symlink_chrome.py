#!/usr/bin/env python3
# 3.2.0
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

try:
    from python.private.chrome_symlinks import ChromeSymlinks
except ImportError:
    print('Missing config file, see python/template/chrome_symlinks.py')
    raise SystemExit(1)


class Symlink:
    def __init__(self):
        self.__bin = Path.home() / '.bin'

        self.symlink_main()

    def symlink_main(self):
        os.chdir(self.__bin)

        for f in ChromeSymlinks.CHROME_SYMLINKS:
            real = Path(f.real)
            symlink = Path(f.symlink)

            if Path.is_symlink(symlink):
                continue
            else:
                os.symlink(real, symlink)


def main():
    Symlink()
