#!/usr/bin/env python3
# 3.0.0
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

try:
    from python.private.chrome_symlinks import Symlinks
except ImportError:
    print('Missing config file, see python/template/chrome_symlinks.py')
    raise SystemExit(1)


class Symlink:
    def __init__(self):
        self.__bin = Path.home() / '.bin'

    def symlink_main(self):
        os.chdir(self.__bin)

        for f in Symlinks.CHROME_SYMLINKS:
            real = Path(f[0])
            symlink = Path(f[1])

            if Path.is_symlink(symlink):
                continue
            else:
                os.symlink(real, symlink)

    def run(self):
        self.symlink_main()


def main():
    run = Symlink()
    run.run()
