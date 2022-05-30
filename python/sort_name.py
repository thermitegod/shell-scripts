#!/usr/bin/env python3

# Copyright (C) 2018-2022 Brandon Zorn <brandonzorn@cock.li>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# SCRIPT INFO
# 3.10.0
# 2021-04-29


import argparse
import sys
from pathlib import Path

from loguru import logger

from utils import confirm

try:
    from private.sort_list import SortList
except ImportError:
    print('Missing config file, see python/template/sort_list.py')
    raise SystemExit(1)


class Sort:
    def __init__(self, args: argparse = None):
        self.__disable_fallback = False

        self.__list_sort = None
        self.__dest = None

        self.__test_dir = Path() / '/tmp/test'

        self.__file_list_done = []
        self.__file_list = []
        for f in Path(Path.cwd()).iterdir():
            if f.is_file():
                self.__file_list.append(f)

        self.__sort_table = SortList.Sort_Table

        self.__total_after = None
        self.__total_before = len(self.__file_list)

        self.parse_args(args=args)

    def sort(self):
        if self.__total_before == 0:
            logger.info(f'No files found')
            raise SystemExit

        for idx, item in enumerate(self.__list_sort):
            if len(self.__file_list) == 0:
                break

            pattern = item.pattern
            save_override = item.save_override

            pattern_glob = pattern.replace(' ', r'*').lower()
            if save_override:
                pattern_target_dir = Path() / save_override
            else:
                pattern_target_dir = Path() / pattern.replace(' ', '-')

            logger.trace(f'====================')
            logger.trace(f'Name\t: {pattern}')
            logger.trace(f'Glob\t: {pattern_glob}')
            logger.trace(f'Dest\t: {pattern_target_dir}')
            logger.trace(f'IDX\t: {idx}')

            for f in self.__file_list:
                # case insensitive pattern matching
                fake_file = Path(str(f).lower())
                if not fake_file.match(f'*{pattern_glob}*'):
                    continue

                file = Path(f)
                target = Path(self.__dest, pattern_target_dir).resolve()
                if not Path.exists(target):
                    # all target dirs should exits before running
                    # otherwise you are going to have a bad time
                    target.mkdir(parents=True, exist_ok=True)

                if not Path.is_file(Path(target, file.name)):
                    # move maches to dest
                    Path.rename(file, Path(target, file.name))
                else:
                    # file already exists in dest so sort into CWD, has to be delt w/ manually
                    if self.__disable_fallback:
                        continue

                    logger.info(f'fallback used for: {f}')
                    fallback_path = Path() / Path.cwd() / pattern_target_dir
                    if not Path.exists(fallback_path):
                        pattern_target_dir.mkdir(parents=True, exist_ok=True)
                    if not Path.is_file(Path(fallback_path, file.name)):
                        Path.rename(file, Path(fallback_path, file.name))
                    else:
                        # fallback path has to already have the same filename in it already
                        logger.warning(f'Unable to sort: {f}')

                self.__file_list_done.append(f)

            for f in self.__file_list_done:
                self.__file_list.remove(f)
            self.__file_list_done = []

    def main(self, sort_list: str, sort_confirm: bool):
        if sort_confirm:
            print(f'Prerun info\n'
                  f'TABLE\t\t: {sort_list}\n'
                  f'Running from\t: {Path.cwd()}\n'
                  f'Dest is\t\t: {self.__dest}\n'
                  '\nMake sure everything has been processed correctly\n')

            if not confirm.confirm_run():
                print('Did not confirm, Exiting')
                raise SystemExit(1)

        self.sort()

        self.__total_after = len(self.__file_list)

        print(f'\nTotal sorted')
        print(f'Before\t: {self.__total_before}')
        print(f'After\t: {self.__total_after}')
        print(f'Total\t: {self.__total_before - self.__total_after}')

    def parse_args(self, args):
        if args.test:
            self.__dest = self.__test_dir
        if args.print:
            print(f'IDX\tENTRIES\t\tTABLE')
            print('====================================')
            for idx, item in enumerate(self.__sort_table, start=1):
                try:
                    entries = len(self.__sort_table[item].sort_list)
                except AttributeError:
                    entries = 0

                print(f'{idx}\t{entries}\t\t{item}')
            raise SystemExit
        if args.sort_table:
            if args.sort_table > len(self.__sort_table):
                print(f'No sorting table exists at position: {args.sort_table}')
                raise SystemExit

            for idx, item in enumerate(self.__sort_table, start=1):
                if not args.sort_table == idx:
                    continue

                try:
                    self.__list_sort = self.__sort_table[item].sort_list
                    self.__disable_fallback = self.__sort_table[item].sort_disable_fallback

                    if self.__dest is None:
                        self.__dest = self.__sort_table[item].sort_dest

                    self.main(sort_list=item, sort_confirm=self.__sort_table[item].sort_confirm)
                except AttributeError:
                    print(f'Empty or malformed list was chosen: {item}')


def main():
    parser = argparse.ArgumentParser(description='Sort files in CWD')
    parser.add_argument('-T', '--test',
                        action='store_true',
                        help='Use test dir as dest \'/tmp/test\'')
    required = parser.add_argument_group('required exclusive arguments').add_mutually_exclusive_group(required=True)
    required.add_argument('-s', '--sort-table',
                          metavar='SORT',
                          type=int,
                          help='Choose sorting table to use')
    required.add_argument('-p', '--print',
                          action='store_true',
                          help='Print available sorting lists')
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

    Sort(args=args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
