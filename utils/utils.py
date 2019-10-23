# -*- coding: utf-8 -*-
# 1.1.0
# 2019-10-23


import os
import os.path
import shlex
import subprocess
import sys
import hashlib


def is_root():
    if os.geteuid() is not 0:
        exit('Requires root, exiting')


def is_not_root():
    if os.geteuid() is 0:
        exit('Do not run as root, exiting')


def run_cmd(cmd):
    subprocess.run(shlex.split(cmd))


def get_script_name():
    return os.path.basename(sys.argv[0])


def not_implemented():
    exit('Not implemented')


def edit_conf(path):
    run_cmd(f'{os.environ.get("EDITOR")} {path}')
    exit(0)


def get_extra_dir():
    return os.path.join(os.environ.get('HOME'), '.bin/bin-extra')


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
