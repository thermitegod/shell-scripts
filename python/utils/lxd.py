# -*- coding: utf-8 -*-
# 1.4.0
# 2020-11-21

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

from loguru import logger

from python.utils.execute import Execute


class _Lxd:
    def __init__(self):
        super().__init__()

        self.base_container = 'dev-gentoo-clang-minimal'
        self.base_rutorrent = 'base-gentoo-rutorrent'
        self.base_transmission = 'base-gentoo-transmission'

    @staticmethod
    def get_state(container: str):
        state = Execute(f'lxc info {container} 2>|/dev/null | grep Running', sh_wrap=True, to_stdout=True).get_out()

        if 'Running' in state:
            logger.debug(f'container state is running for {container}')
            return True
        logger.debug(f'container state is stopped for {container}')
        return False


Lxd = _Lxd()
