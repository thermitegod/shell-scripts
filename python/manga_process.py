# -*- coding: utf-8 -*-
# 1.8.0
# 2021-01-13

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
import time

from python.utils.execute import Execute


class Process:
    def __init__(self):
        self.__mode = 'manga'

        self.__directories = True

        self.__time_start = 0
        self.__time_end = 0

        self.__archivetype = None
        self.__set_compressor_interactive = False

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
            nest_dirs = Execute('find . -mindepth 2 -path \'*/*\' -type d', to_stdout=True).get_out()
            if nest_dirs:
                print(f'Nested directories detected\n\n{nest_dirs}\n\n')

        if self.__remove_junk:
            Execute('remove-junk-files -l')
            Execute('remove-junk-files -Ar')

        detected_credits = Execute('remove-manga-credits -l', to_stdout=True).get_out()
        if detected_credits:
            print(f'{detected_credits}\n\n')
            if self.__mode == 'alt':
                input('Enter to remove found credits')
                if self.__match_zzz:
                    Execute('remove-manga-credits -mz')
                else:
                    Execute('remove-manga-credits -m')
            else:
                print('Printing found, will NOT remove, use -m to remove')

        if self.__numerical_rename:
            Execute(f'rename-numerical-batch')

        if self.__mime_check:
            Execute(f'mime-correct -A')
            print('\n\n')

        print(f'\n\nMode is \'{self.__mode}\'\n\n')
        Execute('count-archive')
        Execute('count-image')
        size = Execute('du -h | tail -n1 | awk \'{print $1}\'', sh_wrap=True, to_stdout=True).get_out().strip('\n')
        print(f'\nSize : {size}\n')

        if self.__set_compressor_interactive:
            print('Choose archive type [DEFAULT:1]\n'
                  '1: zip destructive junkpath\n'
                  '2: zip destructive nojunkpath\n'
                  '3: 7z destructive nojunkpath\n'
                  '4: tar destructive junkpath\n')
            self.__archivetype = input()

            if not self.__archivetype:
                self.__archivetype = 1
            else:
                try:
                    self.__archivetype = int(self.__archivetype)
                    if self.__archivetype > 3:
                        print('Input is out of range')
                        raise SystemExit(1)
                except ValueError:
                    print('Input does not match supported values')
                    raise SystemExit(1)

        self.get_time(start=True)

        if self.__optimize:
            Execute('optimize-all -Mv')

        if self.__archivetype == 1:
            Execute('mkzip -dzP')
        elif self.__archivetype == 2:
            Execute('mkzip -dZjP')
        elif self.__archivetype == 3:
            Execute('mk7z -dzP')
        elif self.__archivetype == 4:
            Execute('mktar -dzj')

        if self.__comp_advzip and not self.__archivetype == 3:
            # does not need to be run for 7z
            # Execute('mkadvzip')
            pass

        if self.__comp_test:
            Execute('mk7z -t -- *', sh_wrap=True)

        if self.__show_time:
            self.get_time(start=False)
            print('\n\n\n'
                  f'Start : {self.__time_start}\n'
                  f'End   : {self.__time_end}\n\n')

    def run(self, args):
        # general
        if args.numerical:
            self.__numerical_rename = True
        if args.not_manga:
            self.__mode = 'alt'
        if args.compression == 0:
            self.__set_compressor_interactive = True
        else:
            self.__archivetype = args.compression
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
    parser.add_argument('-c', '--compression',
                        action='store',
                        type=int,
                        nargs=1,
                        metavar='COMP',
                        default=1,
                        choices=[0, 1, 2, 3, 4],
                        help='Sets default compression for dirs, use \'0\' to get interactive and compressor list')
    parser.add_argument('-r', '--numerical',
                        action='store_true',
                        help='Enable numerical renaming')
    parser.add_argument('-m', '--not-manga',
                        action='store_true',
                        help='Enable the not manga mode')
    parser.add_argument('-z', '--match-zzz',
                        action='store_true',
                        help='Match zzz in credits')
    disable = parser.add_argument_group('disable')
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

    run = Process()
    run.run(args)
