#!/usr/bin/env python3
# 4.0.0
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

import argparse
import os
import os.path
import shutil

from tempfile import TemporaryDirectory

from utils import utils


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clean',
                        action='store_true',
                        help='clean only /usr/src/linux symlink')
    parser.add_argument('-r', '--rm',
                        action='store_true',
                        help='remove all /usr/src/linux/*')
    args = parser.parse_args()

    utils.is_root()

    src = '/usr/src/'

    if args.rm:
        ksym = src + 'linux'
        if os.path.exists(ksym) and os.path.islink(ksym):
            os.unlink(ksym)

        for dirs in next(os.walk(src))[1]:
            kernel = src + dirs
            shutil.rmtree(kernel)
    elif args.clean:
        kdir = src + 'linux'
        if not os.path.exists(kdir):
            exit('Missing kernel symlink')

        if os.path.exists(kdir + '/.config'):
            with TemporaryDirectory() as tmpdir:
                cmd = f'sh -c "cd {kdir};mv .config {tmpdir};make distclean;mv {tmpdir}/.config ."'
                utils.run_cmd(cmd)
        else:
            cmd = f'sh -c "cd {kdir};make distclean"'
            utils.run_cmd(cmd)


if __name__ == "__main__":
    main()
