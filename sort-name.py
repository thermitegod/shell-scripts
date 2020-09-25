#!/usr/bin/env python3
# 1.0.0
# 2020-09-24

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

from utils import utils
from utils import dirs


class Sort:
    def __init__(self):
        self.__list_final = dirs.get_extra_dir() / 'sort-name-final'
        self.__list_type = dirs.get_extra_dir() / 'sort-name-type'

        self.__dest_final = dirs.get_extra_dir() / 'sort-name-final'
        self.__dest_type = dirs.get_extra_dir() / 'sort-name-type'

        self.__list_sort = None
        self.__dest = None

        self.__test_dir = Path() / '/tmp/test'

        self.__sort_name = None
        self.__sort_override = None

        self.__job = None

        self.__total_after = 0
        self.__total_before = utils.run_cmd("ls -1A | wc -l", sh_wrap=True, to_stdout=True)

    def get_dest_dir(self, dest_file):
        for line in Path.open(dest_file):
            line = line.strip('\n').split(' ')
            if line[0].startswith('#'):
                continue

            if line[0].startswith('save_dir'):
                if self.__dest != self.__test_dir:
                    self.__dest = line[1]
                    logger.debug(f'Setting dest dir: {line[1]}')
                continue

    def main_sort(self):
        for line in Path.open(self.__list_sort):
            line = line.strip('\n').split(' ')
            if line[0].startswith('#'):
                # logger.debug(f'Skipping comment: {line}')
                continue

            self.__sort_name = line[0]

            try:
                self.__sort_override = line[1]
            except IndexError:
                self.__sort_override = None

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
            utils.run_cmd(f'find . -maxdepth 1 -type f -iname "*{arc}*" '
                          f'-exec mkdir -p -- "{self.__dest}/{move_to_dir}" \\; -quit')
        elif self.__job == 'sort_main':
            utils.run_cmd(f'find . -maxdepth 1 -type f -iname "*{arc}*" '
                          f'-exec mv -n -- "{{}}" "{self.__dest}/{move_to_dir}" \\;')
        elif self.__job == 'sort_local':
            utils.run_cmd(f'find . -maxdepth 1 -type f -iname "*{arc}*" '
                          f'-exec mkdir -p -- "{Path.cwd()}/{move_to_dir}" \\;'
                          f'-exec mv -i -- "{{}}" "{Path.cwd()}/{move_to_dir}" \\;')

    def main(self):
        print(f'Prerun info')
        print(f'MODE\t\t: {Path(self.__list_sort).name}')
        print(f'Running from\t: {Path.cwd()}')
        print(f'Dest is\t\t: {self.__dest}')
        print('\nMake sure everything has been processed correctly')
        print(f'\nRunning script is: {utils.get_script_name()}\n')
        confirm = input('Confirm run [yn]? ')
        if confirm == 'y':
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
            utils.die(msg='Did not confirm, Exiting')

    def run(self, args):
        # general
        if args.test:
            self.__dest = self.__test_dir
        if args.edit_type:
            utils.edit_conf(self.__list_final)
        if args.edit_final:
            utils.edit_conf(self.__list_type)
        if args.final:
            self.__list_sort = self.__list_final
            if not self.__dest:
                self.get_dest_dir(self.__dest_final)
        if args.type:
            self.__list_sort = self.__list_type
            if not self.__dest:
                self.get_dest_dir(self.__dest_type)

        self.main()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-T', '--test',
                        action='store_true',
                        help='Use test dir as dest \'/tmp/test\'')
    edit = parser.add_argument_group('EDIT')
    edit.add_argument('-e', '--edit-type',
                      action='store_true',
                      help='')
    edit.add_argument('-E', '--edit-final',
                      action='store_true',
                      help='')
    lst = parser.add_argument_group('EDIT')
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

    utils.args_required_else_help()

    logger.remove()
    logger.add(sys.stdout, level=args.loglevel, colorize=True)

    run = Sort()
    run.run(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
