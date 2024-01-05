#!/usr/bin/env python3

# Copyright (C) 2024 Brandon Zorn <brandonzorn@cock.li>
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
# 5.0.0
# 2024-01-04

import os

from pathlib import Path

try:
    from python.private.chrome_symlinks import ChromeSymlinks
except ImportError:
    print('Missing config file, see python/template/chrome_symlinks.py')
    raise SystemExit(1)


class Symlink:
    def __init__(self):
        self.__bin = Path() / os.environ['HOME'] / '.local' / 'bin'

        self.symlink_main()

    def symlink_main(self):
        os.chdir(self.__bin)

        for f in ChromeSymlinks.CHROME_SYMLINKS:
            real = Path(f.real)
            symlink = Path(f.symlink)

            if Path.is_symlink(symlink):
                continue

            os.symlink(real, symlink)


def main():
    Symlink()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
