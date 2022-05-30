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
# 2020-09-24


# Taken from <https://github.com/thermitegod/mcomix-lite/blob/master/mcomix/file_provider.py>

import re

# Split into float, int, and characters
NUMERIC_REGEXP = re.compile(r'\d+[.]\d+|\d+|\D+')


def alphanumeric_sort(filenames: list):
    """
    Do an in-place alphanumeric sort of the strings in <filenames>,
    such that for an example "1.jpg", "2.jpg", "10.jpg" is a sorted ordering
    """

    def isfloat(p):
        try:
            return 0, float(p)
        except ValueError:
            return 1, p.lower()

    def keyfunc(s: str):
        x, y, z = s.rpartition('.')
        if z.isdigit():
            # extension with only digital is not extension
            x = f'{x}{y}{z}'
            z = ''
        return [isfloat(p) for p in (*NUMERIC_REGEXP.findall(x), z)]

    filenames.sort(key=keyfunc)
