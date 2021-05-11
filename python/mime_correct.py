# -*- coding: utf-8 -*-
# 1.15.0
# 2021-04-29

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
from pathlib import Path

from loguru import logger

from python.utils.colors import Colors
from python.utils.hash_compare import HashCompare
from python.utils.mimecheck import Mimecheck
from python.utils.recursion import RecursiveExecute


class MimeCorrect:
    def __init__(self, args: argparse = None):
        self.__list_only = False
        self.__rm_hash_collision = False

        self.__check_all = False
        self.__verbose = False

        self.__total_checked = 0
        self.__total_found = 0
        self.__total_corrected = 0
        self.__total_collision = 0

        self.parse_args(args=args)

        if self.__check_all:
            RecursiveExecute(function=self.main)
        else:
            self.main()

        if self.__total_checked > 0:
            print(f'\nTOTAL')
            self.print_totals(self.__total_checked, self.__total_found,
                              self.__total_corrected, self.__total_collision,
                              print_totals=True)

    def main(self):
        checked = 0
        found = 0
        corrected = 0
        collision = 0

        for f in Path.cwd().iterdir():
            if Path.is_dir(f):
                continue

            if not Mimecheck.check_if_image(f):
                logger.debug(f'Skipping non image file: {f}')
                continue

            checked += 1
            self.__total_checked += 1

            mimeext = Mimecheck.get_mimetype_ext(filename=f)

            if 'bmp' in mimeext:
                mimeext = 'bmp'

            if mimeext not in ('jpeg', 'png', 'gif', 'tiff', 'bmp'):
                logger.debug(f'file type not supported: {mimeext}')
                continue

            name = f.stem
            ext = f.suffix[1:]

            if mimeext == 'jpeg' and ext == 'jpg':
                logger.debug(f'Skipping jpg {f}')
                continue

            if mimeext == 'jpeg':
                mimeext = 'jpg'

            if mimeext != ext:
                current_name = Path(f'{name}.{ext}')
                correct_name = Path(f'{name}.{mimeext}')

                if Path.exists(correct_name) and Path.exists(current_name):
                    if HashCompare(correct_name, current_name).results():
                        logger.debug(f'File collision is same file: \'{current_name}\' \'{correct_name}\'')
                    else:
                        logger.debug(f'File collision with different files: \'{current_name}\' \'{correct_name}\'')
                    collision += 1
                    self.__total_collision += 1
                    if self.__rm_hash_collision and not self.__list_only:
                        current_name.unlink()

                    continue
                else:
                    logger.debug(f'Mismatch: {current_name.resolve()}')

                if self.__list_only:
                    found += 1
                    self.__total_found += 1
                    continue

                Path.rename(current_name, correct_name)

                corrected += 1
                self.__total_corrected += 1

        if checked > 0:
            self.print_totals(checked, found, corrected, collision)

    def print_totals(self, checked: int, found: int, corrected: int,
                     collision: int, print_totals: bool = False):
        checked_out = f'{Colors.GRE}Checked{Colors.NC}: {checked}'
        if self.__list_only:
            problematic_out = f'{Colors.YEL}Found{Colors.NC}: {found}'
        else:
            problematic_out = f'{Colors.YEL}Corrected{Colors.NC}: {corrected}'
        collision_out = f'{Colors.RED}Collision{Colors.NC}: {collision}'

        if self.__verbose and not print_totals:
            pwd_out = f'{Colors.BLU}Path{Colors.NC}: {Path.cwd()}'
        else:
            pwd_out = ''

        print(f'{checked_out}\t{problematic_out}\t{collision_out}\t{pwd_out}')

    def parse_args(self, args):
        if args.list:
            self.__list_only = True
        if args.rm_hash_collision:
            self.__rm_hash_collision = True
        if args.verbose:
            self.__verbose = True
        if args.check_all:
            self.__check_all = True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-A', '--check-all',
                        action='store_true',
                        help='run in all sub-dirs of CWD')
    parser.add_argument('-l', '--list',
                        action='store_true',
                        help='list only in $PWD, no corrections')
    parser.add_argument('-r', '--rm-hash-collision',
                        action='store_true',
                        help='if two files collide with the same hash, '
                             'remove the file with the incorrect file extension')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='extra information in reports')
    debug = parser.add_argument_group('debug')
    debug.add_argument('-L', '--loglevel',
                       default='INFO',
                       metavar='LEVEL',
                       type=str.upper,
                       choices=['NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'VERBOSE', 'DEBUG', 'TRACE'],
                       help='Levels: %(choices)s')
    args = parser.parse_args()

    logger.remove()
    logger.add(sys.stdout, level=args.loglevel, colorize=True)

    MimeCorrect(args=args)
