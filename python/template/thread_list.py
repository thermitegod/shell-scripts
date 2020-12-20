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

# copy to python/private/thread_list.py to use

from collections import namedtuple


class _ThreadList:
    def __init__(self):
        Threads = namedtuple('Threads', ['board', 'thread_number', 'save_dir'])

        self.THREADS_4CHAN = (
            # /a/
            Threads('a', '', ''),
            # Threads('a', '', ''),
            # Threads('a', '', ''),

            # /w/
            Threads('w', '', ''),
            # Threads('w', '', ''),
            # Threads('w', '', ''),
        )

        self.THREADS_8KUN = (
            # /tech/
            # Threads('tech', '', ''),
        )


ThreadList = _ThreadList()
