#!/usr/bin/env python3
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

from pathlib import Path


class Symlink:
    def __init__(self):
        self.__bin = Path.home() / '.bin'
        self.__bin_py = Path.home() / '.bin/python'

    def symlink_main(self):
        os.chdir(self.__bin_py)
        for f in Path(Path.cwd()).iterdir():
            if Path.is_dir(f):
                continue

            os.chdir(self.__bin)

            # remove .py, do not use .strip('.py)
            symlink = Path(f.name[:-3])
            real_path = Path() / 'python' / f.name

            if Path.is_symlink(symlink):
                continue

            os.symlink(real_path, symlink)

    def symlink_special(self):
        targets = (
            ('python/4chan-dl.py', '8chan-dl'),

            ('python/chromium-default.py', 'chromium-sandbox'),

            ('python/backup-meta.py', 'backup-chromium'),
            ('python/backup-meta.py', 'backup-user-bin'),
            ('python/backup-meta.py', 'backup-user-config'),
            ('python/backup-meta.py', 'backup-user-local'),

            ('python/count-image.py', 'count-archive'),
            ('python/count-image.py', 'count-video'),

            ('python/madokami-manga.py', 'madokami-manga-publishing'),
            ('python/madokami-manga.py', 'madokami-novels-publishing'),

            ('python/mkzst.py', 'mkgz'),
            ('python/mkzst.py', 'mklz4'),
            ('python/mkzst.py', 'mkxz'),

            ('python/optimize-all.py', 'optimize-gif'),
            ('python/optimize-all.py', 'optimize-jpg'),
            ('python/optimize-all.py', 'optimize-png'),

            ('python/snip.py', 'snip-root'),
        )

        os.chdir(self.__bin)

        for f in targets:
            real = Path(f[0])
            symlink = Path(f[1])

            if Path.is_symlink(symlink):
                continue
            else:
                os.symlink(real, symlink)

    def run(self):
        self.symlink_main()
        self.symlink_special()


def main():
    run = Symlink()
    run.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
