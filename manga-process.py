#!/usr/bin/env python3
# 1.0.0
# 2020-08-19

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
import time

from utils import utils


class Process:
    def __init__(self):
        self.__mode = 'manga'

        self.__input_files = None
        self.__directories = False

        self.__time_start = 0
        self.__time_end = 0

        self.__archivetype = None

        self.__optimize = True
        self.__match_zzz = False
        self.__show_time = True
        self.__comp_test = True
        self.__mime_check = True
        self.__comp_advzip = True
        self.__remove_junk = True
        self.__numerical_rename = False
        self.__detect_nested_dirs = True

    def get_time(self, start: bool):
        current_time = time.strftime("%B %d %H:%M:%S", time.localtime())
        if start:
            self.__time_start = current_time
        else:
            self.__time_end = current_time

    def process_main(self):
        if self.__detect_nested_dirs:
            nest_dirs = utils.run_cmd('find . -mindepth 2 -path \'*/*\' -type d', to_stdout=True)
            if nest_dirs:
                print(f'Nested directories detected\n\n{nest_dirs}\n\n')

        if self.__remove_junk:
            utils.run_cmd('remove-junk-files -l')
            utils.run_cmd('remove-junk-files -Ar')

        detected_credits = utils.run_cmd('remove-manga-credits -l', to_stdout=True)
        if detected_credits:
            print(f'{detected_credits}\n\n')
            if self.__mode == 'alt':
                input('Enter to remove found credits')
                if self.__match_zzz:
                    utils.run_cmd('remove-manga-credits -mz')
                else:
                    utils.run_cmd('remove-manga-credits -m')
            else:
                print('Printing found, will NOT remove, use -m to remove')

        if self.__numerical_rename:
            utils.run_cmd(f'rename-numerical-batch')

        if self.__mime_check:
            utils.run_cmd(f'mime-correct -A')
            print('\n\n')

        print(f'\n\nMode is \'{self.__mode}\'\n\n')
        utils.run_cmd('count-archive')
        utils.run_cmd('count-image')
        size = utils.run_cmd('du -h | tail -n1 | awk \'{print $1}\'', sh_wrap=True, to_stdout=True).strip('\n')
        print(f'\nSize : {size}\n')

        print('Choose archive type [DEFAULT:1]')
        print('1: zip destructive')
        print('2: zip destructive nojunkpath')
        print('3: 7z dir destructive')
        print('')
        archivetype = input()

        if not archivetype:
            archivetype = 1
        else:
            try:
                archivetype = int(archivetype)
                if archivetype > 3:
                    utils.die('Input is out of range')
            except ValueError:
                utils.die('Input does not match supported values')

        self.get_time(start=True)

        if self.__optimize:
            utils.run_cmd('optimize-all -Mv')

        if archivetype == 1:
            utils.run_cmd('mkzip -dzP')
        elif archivetype == 2:
            utils.run_cmd('mkzip -dZjP')
        elif archivetype == 3:
            utils.run_cmd('mk7z -dzP')

        if self.__comp_advzip and not archivetype == 3:
            # does not need to be run for 7z
            utils.run_cmd('mkadvzip')

        if self.__comp_test:
            utils.run_cmd('mk7z -t -- *', sh_wrap=True)

        if self.__show_time:
            self.get_time(start=False)
            print('\n\n')
            print(f'Start : {self.__time_start}')
            print(f'End   : {self.__time_end}\n\n')

    def run(self, args):
        # general
        if args.directories:
            self.__directories = True
        if args.numerical:
            self.__numerical_rename = True
        if args.not_manga:
            self.__mode = 'alt'
        if args.input_files is not None:
            self.__input_files = args.input_files
        # disable
        if args.disable_advzip:
            self.__comp_advzip = False
        if args.disable_nested_dirs:
            self.__detect_nested_dirs = False
        if args.disable_junk:
            self.__remove_junk = False
        if args.disable_mimecheck:
            self.__mime_check = False
        if args.disable_optimize:
            self.__optimize = False
        if args.disable_tests:
            self.__comp_test = False
        if args.disable_time:
            self.__show_time = False
        if args.match_zzz:
            self.__match_zzz = True

        self.process_main()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_files',
                        action='store',
                        type=str,
                        nargs='*',
                        default=None,
                        help=argparse.SUPPRESS)
    parser.add_argument('-d', '--directories',
                        action='store_true',
                        help='Run for all directories in CWD')
    parser.add_argument('-r', '--numerical',
                        action='store_true',
                        help='Enable numerical renaming')
    parser.add_argument('-m', '--not-manga',
                        action='store_true',
                        help='Enable the not manga mode')
    parser.add_argument('-z', '--match-zzz',
                        action='store_true',
                        help='Match zzz in credits')
    disable = parser.add_argument_group('DISABLE')
    disable.add_argument('-A', '--disable-advzip',
                         action='store_true',
                         help='Disable running mkadvzip')
    disable.add_argument('-D', '--disable-nested-dirs',
                         action='store_true',
                         help='Disable nested directory detection')
    disable.add_argument('-R', '--disable-junk',
                         action='store_true',
                         help='Disable junk file removal')
    disable.add_argument('-M', '--disable-mimecheck',
                         action='store_true',
                         help='Disable mime checker')
    disable.add_argument('-O', '--disable-optimize',
                         action='store_true',
                         help='Disable image optimizer')
    disable.add_argument('-T', '--disable-tests',
                         action='store_true',
                         help='Disable compressed file test')
    disable.add_argument('-t', '--disable-time',
                         action='store_true',
                         help='Disable time total')
    args = parser.parse_args()

    utils.args_required_else_help()

    run = Process()
    run.run(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
