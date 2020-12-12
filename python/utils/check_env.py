# -*- coding: utf-8 -*-
# 2.0.0
# 2020-12-12

# Copyright (C) 2019,2020 Brandon Zorn <brandonzorn@cock.li>
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
import sys
from pathlib import Path

from python.utils.colors import Colors
from python.utils.execute import Execute


class _CheckEnv:
    def __init__(self):
        super().__init__()

        self.__script_args = sys.argv

    @staticmethod
    def root_check(require_root: bool):
        """
        :param require_root:
            If True, running as root is required otherwise will terminate.
            If False, running as root will terminate.
        """

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

    def get_script_name(self):
        return Path(self.__script_args[0]).name

    def args_required_else_help(self):
        try:
            self.__script_args[1]
        except IndexError:
            Execute(f'{self.__script_args[0]} -h')
            raise SystemExit


CheckEnv = _CheckEnv()
