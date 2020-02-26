# -*- coding: utf-8 -*-
# 1.3.0
# 2019-10-31

# Copyright (C) 2019 Brandon Zorn <brandonzorn@cock.li>
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
import hashlib


def is_root():
    if os.geteuid() != 0:
        exit('Requires root, exiting')


def is_not_root():
    if os.geteuid() == 0:
        exit('Do not run as root, exiting')


def run_cmd(cmd):
    subprocess.run(shlex.split(cmd))


def get_script_name():
    return os.path.basename(sys.argv[0])


def not_implemented():
    exit('Not implemented')


def edit_conf(path, e=True):
    run_cmd(f'{os.environ.get("EDITOR")} {path}')
    if e:
        exit(0)


def die(message=None):
    print(f'{message}')
    sys.exit(1)


def get_extra_dir():
    return os.path.join(os.environ['XDG_DATA_HOME'], 'shell')


def hash_compare_sha1(file1, file2):
    hash = []
    for filename in [file1, file2]:
        hasher = hashlib.sha1()
        with open(filename, 'rb') as f:
            hasher.update(f.read())
            hash.append(hasher.hexdigest())

    if hash[0] == hash[1]:
        return True
    return False


def link_check(link):
    if not link[:4] == 'http':
        exit(f'Invalid URL: {link}')
