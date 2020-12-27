# -*- coding: utf-8 -*-
# 3.0.0
# 2020-12-26

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
from pathlib import Path


class _SortList:
    def __init__(self):
        """
        Pattern format
        ('patern', None'),
        ('patern2', 'override'),
        ('patern-3', None),
        # =============
        # first entry will match *pattern* and be saved to pattern
        # second entry will match *pattern2* and be saved to override
        # third entry will match *pattern*3* and be saved to pattern-3
        """

        super().__init__()

        Format = namedtuple('Format', ['sort_dest', 'sort_confirm', 'sort_disable_fallback', 'sort_list'])
        Sort = namedtuple('Sort', ['pattern', 'save_override'])

        self.Sort_Table = {
            'NAME_FINAL':
                Format(
                    sort_dest=Path('./sort').resolve(),
                    sort_confirm=True,
                    sort_disable_fallback=False,
                    sort_list=(
                        Sort('', None),
                        Sort('', None),
                    ),
                ),
            'NAME_TYPE':
                Format(
                    sort_dest=Path('./sort').resolve(),
                    sort_confirm=True,
                    sort_disable_fallback=False,
                    sort_list=(
                        Sort('', None),
                        Sort('', None),
                    ),
                ),
            'IMG_EXT':
                Format(
                    sort_dest=Path.cwd(),
                    sort_confirm=False,
                    sort_disable_fallback=True,
                    sort_list=(
                        Sort('', None),
                        Sort('', None),
                    ),
                ),
            'EMPTY4': None,
            'EMPTY5': None,
            'EMPTY6': None,
            'EMPTY7': None,
            'EMPTY8': None,
            'EMPTY9': None,
        }


SortList = _SortList()
