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
# 1.0.0
# 2021-10-19


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
