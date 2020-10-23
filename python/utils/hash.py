# -*- coding: utf-8 -*-
# 1.2.0
# 2020-10-23

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

import xxhash

from pathlib import Path


def file_hash_compare(file1: Path, file2: Path):
    hash_list = []
    for filename in [file1, file2]:
        hasher = xxhash.xxh3_64()
        with Path.open(filename, 'rb') as f:
            hasher.update(f.read())
            hash_list.append(hasher.hexdigest())

    if hash_list[0] == hash_list[1]:
        return True
    return False
