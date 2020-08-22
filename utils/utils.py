# -*- coding: utf-8 -*-
# 1.12.0
# 2020-08-21

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
import shlex
import subprocess
import sys
from pathlib import Path

from . import colors


def root_check(require_root):
    """
    :param require_root:
        If True, running as root is required otherwise will terminate.
        If False, running as root will terminate.
    """
    c = colors.Colors()
    if require_root:
        if os.geteuid() != 0:
            die(msg=f'{c.BRED}\n\nRequires root, exiting\n\n{c.NC}')
    else:
        if os.geteuid() == 0:
            die(msg=f'{c.BRED}\n\nDo not run as root, exiting\n\n{c.NC}')


def run_cmd(cmd):
    subprocess.run(shlex.split(cmd))


def write_script_shell(path, text):
    script = '#!/usr/bin/env sh\n' \
             f'die(){{ /bin/echo -e $*;kill {os.getpid()};exit; }}\n' \
             f'{text}'

    script_path = Path(path)
    script_path.write_text(script)
    Path.chmod(script_path, 0o700)


def get_script_name():
    return Path(sys.argv[0]).name


def args_required_else_help():
    try:
        sys.argv[1]
    except IndexError:
        run_cmd(f'{sys.argv[0]} -h')
        raise SystemExit


def not_implemented():
    die(msg='Not implemented')


def edit_conf(path, e=True):
    run_cmd(f'{os.environ["EDITOR"]} {path}')
    if e:
        raise SystemExit


def die(msg=None, exit_code=1):
    if msg is not None:
        print(msg)
    raise SystemExit(exit_code)


def link_check(link):
    if not link[:4] == 'http':
        die(msg=f'Invalid URL: {link}')
