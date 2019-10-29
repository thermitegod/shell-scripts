#!/usr/bin/env python3
# 3.0.0
# 2019-10-24

# Copyright (C) 2018,2019 Brandon Zorn, brandonzorn@cock.li
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
import os.path
import shutil

from tempfile import TemporaryDirectory

from utils import utils


def main():
    utils.is_root()

    with TemporaryDirectory() as tmpdir:
        cfgold = '/boot/grub/grub.cfg'
        cfgnew = f'{tmpdir}/grub.cfg'

        cmd = f'grub-mkconfig -o {cfgnew}'
        utils.run_cmd(cmd)

        if not os.path.isfile(cfgnew):
            exit('grub did not create new cfg file')

        if not utils.hash_compare_sha1(cfgold, cfgnew):
            os.unlink(cfgold)
            shutil.move(cfgnew, cfgold)
        else:
            # print('No changes')
            pass


if __name__ == "__main__":
    main()
