# -*- coding: utf-8 -*-
# 2.0.0
# 2020-12-12

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

import xxhash


class HashCompare:
    def __init__(self, file1: Path, file2: Path):
        super().__init__()

        self.__hash_results = None

        hash_list = []
        for filename in [file1, file2]:
            hasher = xxhash.xxh3_64()
            with Path.open(filename, 'rb') as f:
                hasher.update(f.read())
                hash_list.append(hasher.hexdigest())

        if hash_list[0] == hash_list[1]:
            self.__hash_results = True
        self.__hash_results = False

    def results(self):
        return self.__hash_results
