# -*- coding: utf-8 -*-
# 1.9.0
# 2020-04-24

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

import hashlib
import os
import shlex
import subprocess
import sys
from pathlib import Path


def is_root():
    if os.geteuid() != 0:
        die(msg='Requires root, exiting')


def is_not_root():
    if os.geteuid() == 0:
        die(msg='Do not run as root, exiting')


def run_cmd(cmd):
    try:
        subprocess.run(shlex.split(cmd))
    except KeyboardInterrupt:
        print()


def write_script_shell(path, text, inc_die=True):
    if inc_die:
        script = '#!/usr/bin/env sh\n' \
                 f'die(){{ /bin/echo -e $*;kill {os.getpid()};exit; }}\n' \
                 f'{text}'
    else:
        script = '#!/usr/bin/env sh\n' \
                 f'{text}'

    Path(path).write_text(script)
    Path.chmod(Path(path), 0o700)


def get_script_name():
    return Path(sys.argv[0]).name


def args_required_else_help():
    try:
        sys.argv[1]
    except IndexError:
        run_cmd(f'{sys.argv[0]} -h')
        exit()


def not_implemented():
    die(msg='Not implemented')


def edit_conf(path, e=True):
    run_cmd(f'{os.environ["EDITOR"]} {path}')
    if e:
        exit(0)


def die(msg=None, exit_code=1):
    if msg is not None:
        print(msg)
    sys.exit(exit_code)


def get_extra_dir():
    return Path() / os.environ['XDG_DATA_HOME'] / 'shell'


def hash_compare_sha1(file1, file2):
    hash = []
    for filename in [file1, file2]:
        hasher = hashlib.sha1()
        with Path.open(filename, 'rb') as f:
            hasher.update(f.read())
            hash.append(hasher.hexdigest())

    if hash[0] == hash[1]:
        return True
    return False


def link_check(link):
    if not link[:4] == 'http':
        die(msg=f'Invalid URL: {link}')
