# -*- coding: utf-8 -*-
# 4.5.0
# 2021-04-29

# Copyright (C) 2019,2020,2021 Brandon Zorn <brandonzorn@cock.li>
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
from pathlib import Path

from python.utils.execute import Execute
from python.utils.root_check import RootCheck


class Install:
    def __init__(self, args: argparse = None):
        self.__verbose = 'quiet'
        self.__kernel_ebuild = 'sys-kernel/gentoo-sources'

        self.run(args=args)

    def run(self, args):
        if args.verbose:
            self.__verbose = 'verbose'

        if args.git:
            self.__kernel_ebuild = 'sys-kernel/git-sources'
        elif args.vanilla:
            self.__kernel_ebuild = 'sys-kernel/vanilla-sources'

        Execute(f'emerge --ignore-default-opts --oneshot --{self.__verbose} {self.__kernel_ebuild}')

        kernel_config = Path() / '/proc/config.gz'
        if Path.is_file(kernel_config):
            Execute(f'zcat {kernel_config} >| /usr/src/linux/.config', sh_wrap=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='verbose install')
    group1 = parser.add_argument_group('kernels', 'default kernel to install is sys-kernel/gentoo-sources')
    group1.add_argument('-G', '--git',
                        action='store_true',
                        help='install sys-kernel/git-sources')
    group1.add_argument('-V', '--vanilla',
                        action='store_true',
                        help='install sys-kernel/vanilla-sources')
    args = parser.parse_args()

    RootCheck(require_root=True)

    Install(args=args)
