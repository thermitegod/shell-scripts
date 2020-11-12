#!/usr/bin/env python3
# 2.0.0
# 2020-11-11

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

    def write_stubs(self):
        os.chdir(self.__bin_py)
        for f in Path(Path.cwd()).iterdir():
            if Path.is_dir(f):
                continue

            os.chdir(self.__bin)

            # remove .py, do not use .strip('.py)
            script = Path(f.name[:-3])
            stub_file = Path(f.name[:-3].replace('_', '-'))

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
        # (real, symlink)
        targets = (
            # ('4chan-dl', '8chan-dl'),

            ('chromium-default', 'chromium-sandbox'),

            ('backup-meta', 'backup-chromium'),
            ('backup-meta', 'backup-user-bin'),
            ('backup-meta', 'backup-user-config'),
            ('backup-meta', 'backup-user-local'),

            ('count-image', 'count-archive'),
            ('count-image', 'count-video'),

            ('madokami-manga', 'madokami-manga-publishing'),
            ('madokami-manga', 'madokami-novels-publishing'),

            ('mkzst', 'mkgz'),
            ('mkzst', 'mklz4'),
            ('mkzst', 'mkxz'),

            ('optimize-all', 'optimize-gif'),
            ('optimize-all', 'optimize-jpg'),
            ('optimize-all', 'optimize-png'),

            ('snip', 'snip-root'),
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
        self.write_stubs()
        self.symlink_special()


def main():
    run = Symlink()
    run.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
