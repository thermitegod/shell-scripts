# -*- coding: utf-8 -*-
# 2.2.0
# 2021-10-19

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

from loguru import logger

from python.utils.colors import Colors


class RootCheck:
    def __init__(self, require_root: bool = True):
        """
        Can bypass not allowing root to run scripts by setting env var PY_IGNORE_ROOT_CHECK
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
            try:
                if os.environ['PY_IGNORE_ROOT_CHECK']:
                    logger.warning(f'PY_IGNORE_ROOT_CHECK has been set, ignoring root check')
                    return
            except KeyError:
                pass

            if not os.geteuid() == 0:
                return
            msg = 'Do not run as root, exiting\n\nTo bypass root check use: PY_IGNORE_ROOT_CHECK=1'

        print(f'{Colors.BRED}\n\n{msg}\n\n{Colors.NC}')
        raise SystemExit(1)
