# -*- coding: utf-8 -*-
# 1.1.0
# 2020-09-15

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

from . import utils


def get_state(container: str):
    state = utils.run_cmd(f'sh -c "lxc info {container} 2>|/dev/null | grep Running"', to_stdout=True)

    if 'Running' in state:
        logger.debug(f'container state is running for {container}')
        return True
    logger.debug(f'container state is stopped for {container}')
    return False
