# -*- coding: utf-8 -*-

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
# 3.3.0
# 2021-01-04


from collections import namedtuple
from pathlib import Path


class _SortList:
    def __init__(self):
        """
        Pattern format, patterns are space delimited
        ('patern', None'),
        ('patern2', 'override'),
        ('patern 3', None),
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
            # replaces sort_image_type.py
                Format(
                    sort_dest=Path.cwd(),
                    sort_confirm=False,
                    sort_disable_fallback=True,
                    sort_list=(
                        Sort('.jpg', 'JPG'),
                        Sort('.jpeg', 'JPEG'),
                        Sort('.jxl', 'JXL'),
                        Sort('.png', 'PNG'),
                        Sort('.gif', 'GIF'),

                        Sort('.webm', 'WEBM'),
                        Sort('.mp4', 'MP4'),
                        Sort('.mkv', 'MKV'),

                        Sort('.zip', 'ZIP'),
                        Sort('.rar', 'RAR'),
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
