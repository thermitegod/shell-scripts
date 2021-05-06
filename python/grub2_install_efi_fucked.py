# -*- coding: utf-8 -*-
# 2.0.0
# 2021-05-06

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
import sys

from loguru import logger

from python.utils.execute import Execute
from python.utils.root_check import RootCheck


class Grub:
    def __init__(self, args=None):
        logger.info('Someone fucked up the boot loader, again')
        Execute('grub-install --target=x86_64-efi --efi-directory=/boot/efi')

        if args.mkconf:
            Execute('kernel-grub')

        logger.info('\n\nCheck below is correct\n\n')
        Execute('/usr/sbin/efibootmgr')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mkconf',
                        action='store_true',
                        help='Rebuild grub.cfg')
    debug = parser.add_argument_group('debug')
    debug.add_argument('-L', '--loglevel',
                       default='INFO',
                       metavar='LEVEL',
                       type=str.upper,
                       choices=['NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'VERBOSE', 'DEBUG', 'TRACE'],
                       help='Levels: %(choices)s')
    args = parser.parse_args()

    RootCheck(require_root=True)

    logger.remove()
    logger.add(sys.stdout, level=args.loglevel, colorize=True)

    Grub(args=args)
