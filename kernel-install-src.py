#!/usr/bin/env python3
# 3.1.0
# 2019-10-23

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

from utils import utils


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='verbose install')
    group1 = parser.add_argument_group('Kernels', 'Default kernel to install is sys-kernel/gentoo-sources')
    group1.add_argument('-G', '--git',
                        action='store_true',
                        help='install sys-kernel/git-sources')
    group1.add_argument('-V', '--vanilla',
                        action='store_true',
                        help='install sys-kernel/vanilla-sources')
    args = parser.parse_args()

    utils.is_root()

    cmd = 'emerge --ignore-default-opts --oneshot'

    if args.verbose:
        cmd += ' --verbose'
    else:
        cmd += ' --quiet'

    if args.git:
        cmd += ' sys-kernel/git-sources'
    elif args.vanilla:
        cmd += ' sys-kernel/vanilla-sources'
    else:
        cmd += ' sys-kernel/gentoo-sources'

    utils.run_cmd(cmd)


if __name__ == "__main__":
    main()
