# -*- coding: utf-8 -*-
# 1.2.0
# 2019-04-08

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

import os
import shutil

from utils import utils


def get_kernel_dir():
    src = '/usr/src/linux'
    if os.path.exists(src):
        return src

    utils.die(msg=f'{src}: is not a valid symlink')


def __kernel_conf_action(src, dst, act):
    if os.path.isdir(src):
        src = f'{src}/.config'

    if os.path.isdir(dst):
        dst = f'{dst}/.config'

    if not os.path.isfile(src):
        utils.die(msg=f'No kernel config found: {src}')

    if os.path.isfile(dst):
        os.remove(dst)

    if act == 'move':
        shutil.move(src, dst)
    elif act == 'copy':
        shutil.copyfile(src, dst)


def kernel_conf_copy(src, dst):
    __kernel_conf_action(src=src, dst=dst, act='copy')


def kernel_conf_move(src, dst):
    __kernel_conf_action(src=src, dst=dst, act='move')
