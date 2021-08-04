# -*- coding: utf-8 -*-
# 3.0.0
# 2021-08-04

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

from pathlib import Path

import xxhash

class HashCompare:
    def __init__(self, file1: Path, file2: Path):
        super().__init__()

        self.__hash_list = [0, 0]
        for idx, filename in enumerate((file1, file2)):
            hasher = xxhash.xxh3_64()
            with Path.open(filename, 'rb') as f:
                hasher.update(f.read())
                self.__hash_list[idx] = hasher.hexdigest()

    def results(self):
        if self.__hash_list[0] == self.__hash_list[1]:
            return True
        return False

    def hash_list(self):
        return self.__hash_list
