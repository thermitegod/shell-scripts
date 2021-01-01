# -*- coding: utf-8 -*-
# 1.3.0
# 2021-01-01

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

import argparse

from python.utils.execute import Execute
from python.utils.root_check import RootCheck


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mkconf',
                        action='store_true',
                        help='Rebuild grub.cfg')
    args = parser.parse_args()

    RootCheck(require_root=True)

    print('Someone fucked up the boot loader, again')
    Execute('grub-install --target=x86_64-efi --efi-directory=/boot/efi')

    if args.mkconf:
        Execute('kernel-grub')

    print('\n\nCheck below is correct\n\n')
    Execute('/usr/sbin/efibootmgr')
