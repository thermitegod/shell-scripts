# -*- coding: utf-8 -*-
# 2.2.0
# 2020-11-21

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
        for items in self.__list_sort:
            self.__sort_name = items[0]
            self.__sort_override = items[1]

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

        # TODO - try to port to native python?
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
        # general
        if args.test:
            self.__use_test_dir = True
            self.__dest = self.__test_dir

        # set sort type
        if args.final:
            self.__mode = 'sort_name_final'
            self.__list_sort = SortList.SORT_NAME_FINAL
            if not self.__dest:
                self.__dest = SortList.SAVE_DIR
        if args.type:
            self.__mode = 'sort_name_type'
            self.__list_sort = SortList.SORT_NAME_TYPE
            if not self.__dest:
                self.__dest = SortList.SAVE_DIR

        self.main()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-T', '--test',
                        action='store_true',
                        help='Use test dir as dest \'/tmp/test\'')
    lst = parser.add_argument_group('RUNNING')
    lst.add_argument('-f', '--final',
                     action='store_true',
                     help='')
    lst.add_argument('-t', '--type',
                     action='store_true',
                     help='')
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
