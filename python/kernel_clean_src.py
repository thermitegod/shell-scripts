# -*- coding: utf-8 -*-
# 5.12.0
# 2021-01-01

# Copyright (C) 2018,2019,2020,2021 Brandon Zorn <brandonzorn@cock.li>
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
import os
import shutil
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from loguru import logger

from python.utils.execute import Execute
from python.utils.kernel import Kernel
from python.utils.root_check import RootCheck


class Clean:
    def __init__(self):
        self.__kdir = Kernel.get_kernel_dir()

    def kernel_rm(self):
        if Path.is_symlink(self.__kdir):
            Path.unlink(self.__kdir)

        for dirs in Path(self.__kdir.parent).iterdir():
            kdirs = Path() / self.__kdir.parent / dirs
            shutil.rmtree(kdirs)

    def kernel_clean(self):
        cmd = 'make distclean'

        if Path.exists(Path() / self.__kdir / '.config'):
            with TemporaryDirectory() as tmpdir:
                tmpdir = Path() / tmpdir
                Kernel.kernel_conf_move(src=self.__kdir, dst=tmpdir)
                os.chdir(self.__kdir)
                Execute(cmd)
                Kernel.kernel_conf_move(src=tmpdir, dst=self.__kdir)
        else:
            os.chdir(self.__kdir)
            Execute(cmd)

    def run(self, args):
        if args.rm:
            self.kernel_rm()
        elif args.clean:
            self.kernel_clean()


def main():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required exclusive arguments').add_mutually_exclusive_group(required=True)
    required.add_argument('-c', '--clean',
                          action='store_true',
                          help='clean only /usr/src/linux symlink')
    required.add_argument('-r', '--rm',
                          action='store_true',
                          help='remove all /usr/src/linux/*')
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

    run = Clean()
    run.run(args)
