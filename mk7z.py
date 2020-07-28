#!/usr/bin/env python3
# 1.0.0
# 2020-07-28

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
import atexit
import os
import shutil
import sys
import tempfile
from pathlib import Path

from utils import utils


class Compress:
    def __init__(self):
        atexit.register(self.remove_tmpdir)
        self.__tmpdir = tempfile.mkdtemp()

        self.__input_files = None
        self.__output_dir = Path.cwd()

        self.__compressing_dir = True

        self.__directories = False
        self.__files = False

        self.__run_tests = True
        self.__file_list = []

        self.__destructive = False

        self.__threads = 'on'

    def remove_tmpdir(self):
        shutil.rmtree(self.__tmpdir)

    def get_files(self):
        if self.__directories or self.__files:
            dir_listing = []
            for f in Path(Path.cwd()).iterdir():
                dir_listing.append(f)

            for f in dir_listing:
                if Path.is_dir(f) and self.__directories:
                    self.__compressing_dir = True
                    self.compress(file=f)
                elif Path.is_file(f) and self.__files:
                    self.__compressing_dir = False
                    self.compress(file=f)
        elif self.__input_files is not None:
            for f in self.__input_files:
                f = Path(f)
                if Path.is_dir(f):
                    self.__compressing_dir = True
                    self.compress(file=f)
                elif Path.is_file(f):
                    self.__compressing_dir = False
                    self.compress(file=f)

        if self.__run_tests:
            for f in self.__file_list:
                utils.run_cmd(f'mk7z -T "{f}"')

    def compress(self, file):
        test_file = Path() / self.__output_dir / f'{file}.7z'
        if Path.exists(test_file):
            print(f'Skipping, archive already exists at: \'{test_file}\'')
            return

        script = f'{self.__tmpdir}/tmp.sh'
        die_failed = f'die "Compression failed for \'{Path.resolve(file)}\'"'

        self.__file_list.append(f'{self.__output_dir}/{Path(file).name}.7z')

        os.chdir(Path(file).parent)

        text = f'nice -19 ' \
               f'7zr a -t7z -m0=lzma2 -md=1024m -mmf=bt4 -mmt={self.__threads} -mmtf={self.__threads} ' \
               f'-myx=9 -mx=9 -mfb=276 -mhc=on -ms=on -mtm=off -mtc=off -mta=off ' \
               f'-o="{self.__output_dir}" "{Path(file).name}.7z" "{Path(file).name}" || {die_failed}'

        utils.write_script_shell(script, text)
        utils.run_cmd(script)
        Path.unlink(Path(script))

        if Path.exists(test_file):
            if self.__destructive:
                if self.__compressing_dir:
                    shutil.rmtree(file)
                else:
                    Path.unlink(file)
        else:
            utils.die(f'ERROR: archive not created for: \'{file}\'')

    def run(self, args):
        # other
        if args.input_files is not None:
            self.__input_files = args.input_files
        if args.disable_tests:
            self.__run_tests = False
        if args.output_dir:
            out = Path.resolve(Path(args.output_dir))
            if not Path.is_dir(out):
                if Path.exists(out):
                    utils.die(msg=f'selected output dir \'{out}\' exists but is not a directory')
                Path(out).mkdir(parents=True, exist_ok=True)
            self.__output_dir = out
        # compression type
        if args.directories:
            self.__directories = True
        if args.files:
            self.__files = True
        # profile
        if args.single:
            self.__threads = 'off'
        if args.multi:
            self.__threads = 'on'
        # tests
        if args.test:
            file_list = ''
            for f in self.__input_files:
                file_list += f'{f} '
            # not a fan of doing this
            utils.run_cmd(f'/usr/local/bin/shell/mk7z -T {file_list}')
            sys.exit(0)
        # destructive
        if args.destructive:
            self.__destructive = True

        self.get_files()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_files',
                        action='store',
                        type=str,
                        nargs='*',
                        default=None,
                        help=argparse.SUPPRESS)
    parser.add_argument('-P', '--disable-tests',
                        action='store_true',
                        help='disable post compression test')
    parser.add_argument('-o', '--output-dir',
                        metavar='DIR',
                        help='create the archive[s] in this directory')
    profile = parser.add_argument_group('PROFILE')
    profile.add_argument('-S', '--single',
                         action='store_true',
                         help='Single threaded, useful when hitting oom with multi')
    profile.add_argument('-M', '--multi',
                         action='store_true',
                         help='Multithreaded [default]')
    batch = parser.add_argument_group('BATCH CREATION')
    batch.add_argument('-d', '--directories',
                       action='store_true',
                       help='compress all directories in cwd')
    batch.add_argument('-f', '--files',
                       action='store_true',
                       help='compress all files in cwd')
    other = parser.add_argument_group('OTHER')
    other.add_argument('-T', '--test',
                       action='store_true',
                       help='Test file[s] passed in $1')
    rm = parser.add_argument_group('DESTRUCTIVE')
    rm.add_argument('-z', '--destructive',
                    action='store_true',
                    help='Delete original after it is compressed')

    args = parser.parse_args()

    utils.args_required_else_help()

    run = Compress()
    run.run(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
