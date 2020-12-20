# -*- coding: utf-8 -*-
# 1.1.0
# 2020-12-20

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

from collections import namedtuple


class _SortList:
    def __init__(self):
        """
        Current format

        ('patern', None'),
        ('patern2', 'override'),
        ('patern-3', None),
        # =============
        # first entry will match *pattern* and be saved to pattern
        # second entry will match *pattern2* and be saved to override
        # third entry will match *pattern*3* and be saved to pattern-3
        """

        Sort = namedtuple('Symlinks', ['pattern', 'save_override'])

        self.SAVE_DIR = './sort'

        self.SORT_NAME_FINAL = (
            Sort('', ''),
            # Sort('', ''),
            # Sort('', ''),
        )

        self.SORT_NAME_TYPE = (
            Sort('', ''),
            # Sort('', ''),
            # Sort('', ''),
        )


SortList = _SortList()
