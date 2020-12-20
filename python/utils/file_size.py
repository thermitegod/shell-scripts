# -*- coding: utf-8 -*-
# 1.0.0
# 2020-12-19

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
from collections import namedtuple


class FileSize:
    def __init__(self, filename: Path):
        super().__init__()

        SizeFormat = namedtuple('SizeFormat', ['size', 'unit_counter', 'unit'])

        n = Path.stat(filename).st_size

        unit_size = 1024.0
        unit_symbols = ('B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB')

        s = 0
        while n >= unit_size:
            s += 1
            n /= unit_size

        self.__formated_size = SizeFormat(int(n), s, f'{unit_symbols[s]}')

    @property
    def size(self):
        return self.__formated_size
