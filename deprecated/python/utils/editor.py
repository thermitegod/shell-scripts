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
# 1.0.0
# 2020-10-04


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
