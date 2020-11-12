# -*- coding: utf-8 -*-
# 1.9.0
# 2020-11-12

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

from python.utils import hash
from python.utils.colors import Colors
from python.utils.mimecheck import Mimecheck
from python.utils.script import Script


class MimeCorrect:
    def __init__(self):
        self.__list_only = False
        self.__rm_hash_collision = False

        self.__verbose = False

    def main(self):
        total = 0
        collision = 0
        fixed = 0

        for f in Path.cwd().iterdir():
            if Path.is_dir(f):
                continue

            if not Mimecheck.check_if_image(f):
                logger.debug(f'Skipping non image file: {f}')
                continue

            total += 1

            mimeext = Mimecheck.get_mimetype_ext(filename=f)

            if 'bmp' in mimeext:
                mimeext = 'bmp'

            if mimeext not in ('jpeg', 'png', 'gif', 'tiff', 'bmp'):
                logger.debug(f'file type not supported: {mimeext}')
                continue

            name_split = str(f.name).rpartition('.')
            name = name_split[0]
            ext = name_split[-1]

            if mimeext == 'jpeg' and ext == 'jpg':
                logger.debug(f'Skipping jpg {f}')
                continue

            if mimeext == 'jpeg':
                mimeext = 'jpg'

            if mimeext != ext:
                current_name = Path(f'{name}.{ext}')
                correct_name = Path(f'{name}.{mimeext}')

                if Path.exists(correct_name) and Path.exists(current_name):
                    if hash.file_hash_compare(correct_name, current_name):
                        logger.debug(f'File collision is same file: \'{current_name}\' \'{correct_name}\'')
                    else:
                        logger.debug(f'File collision with different files: \'{current_name}\' \'{correct_name}\'')
                    collision += 1
                    if self.__rm_hash_collision and not self.__list_only:
                        current_name.unlink()

                    continue
                else:
                    logger.debug(f'Mismatch: {current_name.resolve()}')

                if self.__list_only:
                    continue

                Path.rename(current_name, correct_name)

                fixed += 1

        if total != 0:
            total_out = f'{Colors.GRE}Checked{Colors.NC}: {total}'

            if fixed != 0:
                fixed_out = f'{Colors.YEL}Corrected{Colors.NC}: {fixed}'
            else:
                fixed_out = ''

            if collision != 0:
                collision_out = f'{Colors.RED}Collision{Colors.NC}: {collision}'
            else:
                collision_out = ''

            if self.__verbose:
                pwd_out = f'in: {Path.cwd()}'
            else:
                pwd_out = ''

            print(f'{total_out}\t{fixed_out}\t{collision_out}\t{pwd_out}')
        else:
            logger.debug('total == 0')

    def run(self, args):
        if args.check_all:
            text = f'find {Path.cwd()} -path \'*/*\' -type d \\( ! -name . \\) | ' \
                   f'while read -r dir ; do cd "${{dir}}" && {Path(sys.argv[0])} ; done\n'
            Script.execute_script_shell(text=text)
            raise SystemExit
        if args.list:
            self.__list_only = True
        if args.rm_hash_collision:
            self.__rm_hash_collision = True
        if args.verbose:
            self.__verbose = True

        self.main()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-A', '--check-all',
                        action='store_true',
                        help='run in all sub-dirs of $PWD')
    parser.add_argument('-l', '--list',
                        action='store_true',
                        help='list only in $PWD, no corrections')
    parser.add_argument('-r', '--rm-hash-collision',
                        action='store_true',
                        help='if two files collide with the same sha1 hash, '
                             'remove the file with the incorrect file extension')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='extra information in reports')
    debug = parser.add_argument_group('DEBUG')
    debug.add_argument('-L', '--loglevel',
                       default='INFO',
                       metavar='LEVEL',
                       type=str.upper,
                       choices=['NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'VERBOSE', 'DEBUG', 'TRACE'],
                       help='Levels: %(choices)s')
    args = parser.parse_args()

    # utils.args_required_else_help()

    logger.remove()
    logger.add(sys.stdout, level=args.loglevel, colorize=True)

    run = MimeCorrect()
    run.run(args)
