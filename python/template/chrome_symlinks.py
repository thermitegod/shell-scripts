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


class _ChromeSymlinks:
    def __init__(self):
        Symlinks = namedtuple('Symlinks', ['real', 'symlink'])

        self.CHROME_SYMLINKS = (
            Symlinks('chromium-default', 'chromium-'),
            Symlinks('chromium-default', 'chromium-'),
            # Symlinks('chromium-default', 'chromium-'),
        )


ChromeSymlinks = _ChromeSymlinks()
