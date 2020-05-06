#!/usr/bin/env python3
# 1.0.0
# 2020-05-06

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

import argparse

from utils import utils


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mkconf',
                        action='store_true',
                        help='Rebuild grub.cfg')
    args = parser.parse_args()

    print('Someone fucked up the boot loader, again')
    utils.run_cmd('grub-install --target=x86_64-efi --efi-directory=/boot/efi')

    if args.mkconf:
        utils.run_cmd('kernel-grub')

    print('\n\nCheck below is correct\n\n')
    utils.run_cmd('/usr/sbin/efibootmgr')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
