# -*- coding: utf-8 -*-
# 1.7.0
# 2020-12-13

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

import shutil
from pathlib import Path

from loguru import logger


class _Kernel:
    def __init__(self):
        super().__init__()

        self.__src: Path = Path.resolve(Path('/usr/src/linux'))
        if not Path.exists(self.__src):
            logger.critical(f'{self.__src}: is not a valid symlink')
            raise SystemExit(1)

    def get_kernel_dir(self):
        return self.__src

    @staticmethod
    def _kernel_conf_action(src: Path, dst: Path, act: str):
        # src and dst can be either a directory containing the
        # kernel .config or the full path to the kernel .config
        # if src or dst is a directory then the kernel .config will
        # be appended

        src_config: Path = src
        dst_config: Path = dst

        if Path.is_dir(src_config):
            src_config = Path() / src_config / '.config'

        if Path.is_dir(dst_config):
            dst_config = Path() / dst_config / '.config'

        if not Path.is_file(src_config):
            logger.critical(f'No kernel config found: {src_config}')
            raise SystemExit(1)

        if Path.is_file(dst_config):
            Path.unlink(dst_config)

        if act == 'move':
            shutil.move(src_config, dst_config)
        elif act == 'copy':
            shutil.copyfile(src_config, dst_config)

    def kernel_conf_copy(self, src: Path, dst: Path):
        self._kernel_conf_action(src=src, dst=dst, act='copy')

    def kernel_conf_move(self, src: Path, dst: Path):
        self._kernel_conf_action(src=src, dst=dst, act='move')


Kernel = _Kernel()
