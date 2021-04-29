#!/usr/bin/env python3
# 2.4.0
# 2021-04-29

# Copyright (C) 2020,2021 Brandon Zorn <brandonzorn@cock.li>
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
from collections import namedtuple
from pathlib import Path


class Symlink:
    def __init__(self):
        self.__bin = Path.home() / '.bin'
        self.__bin_py = Path.home() / '.bin/python'

        self.write_stubs()
        self.symlink_special()

    def write_stubs(self):
        os.chdir(self.__bin_py)
        for f in Path(Path.cwd()).iterdir():
            if Path.is_dir(f):
                continue

            os.chdir(self.__bin)

            script = Path(f.name.removesuffix('.py'))
            stub_file = Path(f.name.removesuffix('.py').replace('_', '-'))

            stub = f'#!/usr/bin/env python3\n' \
                   f'from python import {script}\n' \
                   f'try:\n' \
                   f'    {script}.main()\n' \
                   f'except KeyboardInterrupt:\n' \
                   f'    raise SystemExit\n' \

            os.chdir(self.__bin)

            if Path.is_file(stub_file):
                stub_file.unlink()

            stub_file.write_text(stub)
            Path.chmod(stub_file, 0o700)

        # print(stub)

    def symlink_special(self):
        Symlinks = namedtuple('Symlinks', ['real', 'symlink'])

        targets = (
            # ('4chan-dl', '8chan-dl'),

            Symlinks('chromium-default', 'chromium-sandbox'),

            Symlinks('backup-meta', 'backup-chromium'),
            Symlinks('backup-meta', 'backup-user-bin'),
            Symlinks('backup-meta', 'backup-user-config'),
            Symlinks('backup-meta', 'backup-user-local'),

            Symlinks('count-image', 'count-archive'),
            Symlinks('count-image', 'count-video'),

            Symlinks('madokami-manga', 'madokami-manga-publishing'),
            Symlinks('madokami-manga', 'madokami-novels-publishing'),

            Symlinks('mkzst', 'mkgz'),
            Symlinks('mkzst', 'mklz4'),
            Symlinks('mkzst', 'mkxz'),

            Symlinks('optimize-all', 'optimize-gif'),
            Symlinks('optimize-all', 'optimize-jpg'),
            Symlinks('optimize-all', 'optimize-png'),

            Symlinks('snip', 'snip-root'),
        )

        os.chdir(self.__bin)

        for idx, item in enumerate(targets):
            real = Path(item.real)
            symlink = Path(item.symlink)

            if Path.is_symlink(symlink):
                continue
            else:
                os.symlink(real, symlink)


def main():
    Symlink()
