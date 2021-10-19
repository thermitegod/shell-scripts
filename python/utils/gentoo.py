# -*- coding: utf-8 -*-
# 1.0.0
# 2021-10-19

# Copyright (C) 2021 Brandon Zorn <brandonzorn@cock.li>
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

from pathlib import Path

from loguru import logger


class GentooCheck:
    def __init__(self):
        """
        Checks if running os is Gentoo, otherwise exit
        """

        super().__init__()

        if not Path('/etc/gentoo-release').exists():
            logger.critical(f'Script can only be run under Gentoo')
            raise SystemExit
