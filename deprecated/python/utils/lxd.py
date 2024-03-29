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

# SCRIPT INFO
# 1.5.0
# 2020-12-13


from loguru import logger

from utils.execute import Execute


class _Lxd:
    def __init__(self):
        super().__init__()

        self.base_container: str = 'dev-gentoo-clang-minimal'
        self.base_rutorrent: str = 'base-gentoo-rutorrent'
        self.base_transmission: str = 'base-gentoo-transmission'

    @staticmethod
    def get_state(container: str):
        state: str = Execute(f'lxc info {container} 2>|/dev/null | grep Running',
                             sh_wrap=True, to_stdout=True).get_out()

        if 'Running' in state:
            logger.debug(f'container state is running for {container}')
            return True
        logger.debug(f'container state is stopped for {container}')
        return False


Lxd = _Lxd()
