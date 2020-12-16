# -*- coding: utf-8 -*-
# 1.0.0
# 2020-11-09

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

# copy to python/private/thread_list.py to use


class _ThreadList:
    def __init__(self):
        """
        Current format

        # Board
        # thread number
        # relative download path
        """

        self.THREADS_4CHAN = (
            # /a/
            # ('a', '', ''),
            # ('a', '', ''),
            # ('a', '', ''),

            # /w/
            # ('w', '', ''),
            # ('w', '', ''),
            # ('w', '', ''),
        )

        self.THREADS_8KUN = (
            # /tech/
            # ('tech', '', ''),
        )


ThreadList = _ThreadList()
