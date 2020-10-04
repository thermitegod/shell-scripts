# -*- coding: utf-8 -*-
# 1.4.1
# 2020-10-04

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

from utils import utils


def get_kernel_dir():
    src = Path() / '/usr/src/linux'
    if Path.exists(src):
        return src

    utils.die(msg=f'{src}: is not a valid symlink')


def __kernel_conf_action(src: Path, dst: Path, act: str):
    # src and dst can be either a directory containing the
    # kernel .config or the full path to the kernel .config
    # if src or dst is a directory then the kernel .config will
    # be appended

    if Path.is_dir(src):
        src = Path() / src / '.config'

    if Path.is_dir(dst):
        dst = Path() / dst / '.config'

    if not Path.is_file(src):
        utils.die(msg=f'No kernel config found: {src}')

    if Path.is_file(dst):
        Path.unlink(dst)

    if act == 'move':
        shutil.move(src, dst)
    elif act == 'copy':
        shutil.copyfile(src, dst)


def kernel_conf_copy(src: Path, dst: Path):
    __kernel_conf_action(src=src, dst=dst, act='copy')


def kernel_conf_move(src: Path, dst: Path):
    __kernel_conf_action(src=src, dst=dst, act='move')
