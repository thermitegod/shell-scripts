# -*- coding: utf-8 -*-
# 1.27.0
# 2020-11-21

# Copyright (C) 2019,2020 Brandon Zorn <brandonzorn@cock.li>
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
import re
import sys
from pathlib import Path

from python.utils.colors import Colors
from python.utils.execute import Execute


def root_check(require_root: bool):
    """
    :param require_root:
        If True, running as root is required otherwise will terminate.
        If False, running as root will terminate.
    """
    if require_root:
        if os.geteuid() != 0:
            print(f'{Colors.BRED}\n\nRequires root, exiting\n\n{Colors.NC}')
            raise SystemExit(1)
    else:
        if os.geteuid() == 0:
            print(f'{Colors.BRED}\n\nDo not run as root, exiting\n\n{Colors.NC}')
            raise SystemExit(1)


def shell_escape(string: str):
    # to get full shell escape have to use .replace because re.escape will not
    # escape single quotes
    return re.escape(string).replace("'", r"\'")


def get_script_name():
    return Path(sys.argv[0]).name


def args_required_else_help():
    try:
        sys.argv[1]
    except IndexError:
        Execute(f'{sys.argv[0]} -h')
        raise SystemExit
