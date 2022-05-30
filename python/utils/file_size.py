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
# 1.0.0
# 2020-12-19


from collections import namedtuple
from pathlib import Path


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
