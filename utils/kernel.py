# -*- coding: utf-8 -*-
# 1.1.0
# 2019-03-12

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


def move_kernel_conf(src=None, dst=None, act='move'):
    if (src or dst) is None:
        utils.die(msg=f'Missing args for move_kernel_conf()')

    if os.path.isdir(src):
        src = f'{src}/.config'
    if os.path.isdir(dst):
        src = f'{dst}/.config'

    if not os.path.isfile(src):
        utils.die(msg=f'No kernel config found: {src}')

    if os.path.isfile(dst):
        os.remove(dst)

    if act == 'move':
        shutil.move(src, dst)
    elif act == 'copy':
        shutil.copyfile(src, dst)
    else:
        utils.die(msg=f'invalid arg: {act}')



