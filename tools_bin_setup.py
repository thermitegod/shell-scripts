#!/usr/bin/env python3

# Copyright (C) 2024 Brandon Zorn <brandonzorn@cock.li>
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
# 4.0.0
# 2024-01-04


import os
from collections import namedtuple
from pathlib import Path

from python.utils import repo


class Symlink:
    def __init__(self):
        self.__repo_base_path = repo.repo_base_dir()

        self.__bin = Path() / os.environ['HOME'] / '.local' / 'bin'

        self.__bin_sh = self.__repo_base_path / 'shell'
        self.__bin_py = self.__repo_base_path / 'python'

        self.symlink_python()
        self.symlink_python_special()

    def symlink_shell_normal(self):
        os.chdir(self.__bin_sh)
        for f in Path(Path.cwd()).iterdir():
            if Path.is_dir(f):
                continue

            real = Path(f)
            symlink = Path() / self.__bin / real.name.removesuffix('.sh')
            if Path.is_symlink(symlink):
                continue

            # print(f'{symlink} -> {real}')
            os.symlink(real, symlink)

    def symlink_python(self):
        os.chdir(self.__bin_py)
        for f in Path(Path.cwd()).iterdir():
            if Path.is_dir(f):
                continue

            real = Path(f)
            symlink = Path() / self.__bin / real.name.removesuffix('.py').replace('_', '-')
            if Path.is_symlink(symlink):
                continue

            # print(f'{symlink} -> {real}')
            os.symlink(real, symlink)

    def symlink_python_special(self):
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
        )

        os.chdir(self.__bin)

        for idx, item in enumerate(targets):
            real = Path(item.real)
            symlink = Path(item.symlink)

            if Path.is_symlink(symlink):
                continue

            os.symlink(real, symlink)

def main():
    Symlink()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
