# -*- coding: utf-8 -*-
# 3.8.0
# 2020-12-12

# Copyright (C) 2018,2019,2020 Brandon Zorn <brandonzorn@cock.li>
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

import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from python.utils import utils
from python.utils.execute import Execute
from python.utils.hash_compare import HashCompare


def main():
    utils.root_check(require_root=True)

    with TemporaryDirectory() as tmpdir:
        cfg = 'grub.cfg'

        cfgold = Path() / '/boot/grub' / cfg
        cfgnew = Path() / tmpdir / cfg

        cmd = f'grub-mkconfig -o {cfgnew}'
        Execute(cmd)

        if not Path.is_file(cfgnew):
            print('grub did not create new cfg file')
            raise SystemExit(1)

        if Path.exists(cfgold):
            if not HashCompare(cfgold, cfgnew).results():
                Path.unlink(cfgold)
                shutil.move(cfgnew, cfgold)
            else:
                print('No changes')
        else:
            shutil.move(cfgnew, cfgold)
