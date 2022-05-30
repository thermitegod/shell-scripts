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
# 3.0.0
# 2021-01-01


import sys
from pathlib import Path

from utils.execute import Execute


class _CheckEnv:
    def __init__(self):
        super().__init__()

        self.__script_args: list = sys.argv

    def get_script_name(self):
        return Path(self.__script_args[0]).name

    def args_required_else_help(self):
        try:
            self.__script_args[1]
        except IndexError:
            Execute(f'{self.__script_args[0]} -h')
            raise SystemExit


CheckEnv = _CheckEnv()
