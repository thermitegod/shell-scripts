# -*- coding: utf-8 -*-
# 3.0.0
# 2020-12-21

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
import sys
from pathlib import Path

from loguru import logger

from python.utils import confirm
from python.utils.check_env import CheckEnv
from python.utils.execute import Execute

try:
    from python.private.sort_list import SortList
except ImportError:
    print('Missing config file, see python/template/sort_list.py')
    raise SystemExit(1)

# TODO
#   port 'find' commands to native python


class Sort:
    def __init__(self):
        self.__mode = None

        self.__list_sort = None
        self.__dest = None

        self.__use_test_dir = False
        self.__test_dir = Path() / '/tmp/test'

        self.__sort_name = None
        self.__sort_override = None

        self.__job = None

        # self.__total_after = 0
        # self.__total_before = Execute("ls -1A | wc -l", sh_wrap=True, to_stdout=True).get_ret()

    def main_sort(self):
        for idx, item in enumerate(self.__list_sort):
            self.__sort_name = item.pattern
            self.__sort_override = item.save_override

            self.name_sort()

    def name_sort(self):
        arc = self.__sort_name.replace('-', r'*')
        if self.__sort_override:
            move_to_dir = Path() / self.__sort_override
        else:
            move_to_dir = Path() / self.__sort_name

        logger.trace(f'====================')
        logger.trace(f'Name\t: {self.__sort_name}')
        logger.trace(f'Arc\t: {arc}')
        logger.trace(f'Dir\t: {move_to_dir}')

        if self.__job == 'dir_check':
            Execute(f'find . -maxdepth 1 -type f -iname "*{arc}*" '
                    f'-exec mkdir -p -- "{self.__dest}/{move_to_dir}" \\; -quit')
        elif self.__job == 'sort_main':
            Execute(f'find . -maxdepth 1 -type f -iname "*{arc}*" '
                    f'-exec mv -n -- "{{}}" "{self.__dest}/{move_to_dir}" \\;')
        elif self.__job == 'sort_local':
            Execute(f'find . -maxdepth 1 -type f -iname "*{arc}*" '
                    f'-exec mkdir -p -- "{Path.cwd()}/{move_to_dir}" \\;'
                    f'-exec mv -i -- "{{}}" "{Path.cwd()}/{move_to_dir}" \\;')

    def main(self):
        print(f'Prerun info\n'
              f'MODE\t\t: {self.__mode}\n'
              f'Running from\t: {Path.cwd()}\n'
              f'Dest is\t\t: {self.__dest}\n'
              '\nMake sure everything has been processed correctly\n'
              f'\nRunning script is: {CheckEnv.get_script_name()}\n')

        if confirm.confirm_run():
            # all target dirs should exits before running
            # otherwise you are going to have a bad time
            logger.debug(f'running dir_check')
            self.__job = 'dir_check'
            self.main_sort()

            # move maches to dest
            logger.debug(f'running sort_main')
            self.__job = 'sort_main'
            self.main_sort()

            # deal w/ name collisions in dest by sorting into $pwd, to be delt w/ manually
            logger.debug(f'running sort_local')
            self.__job = 'sort_local'
            self.main_sort()
            pass
        else:
            print('Did not confirm, Exiting')
            raise SystemExit(1)

    def run(self, args):
        if args.test:
            self.__use_test_dir = True
            self.__dest = self.__test_dir
        if args.print:
            print(f'IDX\tLIST')
            print('===================')
            for idx, item in enumerate(SortList.Sort_Table, start=1):
                print(f'{idx}\t{item}')
            raise SystemExit
        if args.sort_table:
            for idx, item in enumerate(SortList.Sort_Table, start=1):
                if args.sort_table == idx:
                    self.__mode = item
                    self.__list_sort = SortList.Sort_Table[item]
                    if self.__list_sort is None:
                        print(f'Empty list was choosen: {item}')
                        raise SystemExit
                    if not self.__dest:
                        self.__dest = SortList.SAVE_DIR

        self.main()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sort-table',
                        metavar='SORT',
                        type=int,
                        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9],
                        help='Choose sorting table to use')
    parser.add_argument('-T', '--test',
                        action='store_true',
                        help='Use test dir as dest \'/tmp/test\'')
    parser.add_argument('-p', '--print',
                        action='store_true',
                        help='Print available sorting lists')
    debug = parser.add_argument_group('DEBUG')
    debug.add_argument('-L', '--loglevel',
                       default='INFO',
                       metavar='LEVEL',
                       type=str.upper,
                       choices=['NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'VERBOSE', 'DEBUG', 'TRACE'],
                       help='Levels: %(choices)s')
    args = parser.parse_args()

    CheckEnv.args_required_else_help()

    logger.remove()
    logger.add(sys.stdout, level=args.loglevel, colorize=True)

    run = Sort()
    run.run(args)
