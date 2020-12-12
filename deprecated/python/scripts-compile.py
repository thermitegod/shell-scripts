#!/usr/bin/env python3
# 1.1.0
# 2020-11-21

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

from python.utils.execute import Execute


class Compile:
    def __init__(self):
        self.__bin = Path.home() / '.bin'

    def compile(self):
        os.chdir(self.__bin)
        Execute(f'python -m compileall .')


def main():
    run = Compile()
    run.compile()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
