# -*- coding: utf-8 -*-
# 1.0.0
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

import os

from . import utils

from pathlib import Path


def edit_conf(path: Path, exit_done: bool = True):
    """
    :param path:
        Path to config to edit
    :param exit_done:
        Whether to exit when editing is done
    """

    if Path.exists(path) and not Path.is_file(path):
        print(f'path is not a file: {path}')
        raise SystemExit(1)

    try:
        editor = os.environ['EDITOR']
    except KeyError:
        print(f'EDITOR is not set')
        raise SystemExit(1)

    utils.run_cmd(f'{editor} {path}')

    if exit_done:
        raise SystemExit
