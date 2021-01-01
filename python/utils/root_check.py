# -*- coding: utf-8 -*-
# 1.0.0
# 2021-01-01

# Copyright (C) 2019,2020,2021 Brandon Zorn <brandonzorn@cock.li>
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

import os

from python.utils.colors import Colors


class RootCheck:
    def __init__(self, require_root: bool):
        """
        :param require_root:
            If True, running as root is required otherwise will terminate.
            If False, running as root will terminate.
        """

        super().__init__()

        if require_root:
            if not os.geteuid() != 0:
                return
            msg = 'Requires root, exiting'
        else:
            if not os.geteuid() == 0:
                return
            msg = 'Do not run as root, exiting'

        print(f'{Colors.BRED}\n\n{msg}\n\n{Colors.NC}')
        raise SystemExit(1)
