# -*- coding: utf-8 -*-
# 1.6.0
# 2021-05-06

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

# not using sys-kernel/linux-firmware[initramfs]
# since i only need an img with fam17h

# based on: https://wiki.gentoo.org/wiki/AMD_microcode

import argparse
import os
import shutil
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from loguru import logger

from python.utils.execute import Execute
from python.utils.root_check import RootCheck


class Microcode:
    def __init__(self):
        self.__dir_structure = 'kernel/x86/microcode'
        self.__amd_micro = Path('/lib/firmware/amd-ucode/microcode_amd_fam17h.bin')
        self.__amd_micro_boot = Path('/boot/amd-uc.img')
        self.__amd_micro_name = 'AuthenticAMD.bin'

        self.run()

    def run(self):
        with TemporaryDirectory() as tmpdir:
            full_path = Path() / tmpdir / self.__dir_structure
            full_path.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(self.__amd_micro, Path() / full_path / self.__amd_micro_name)
            os.chdir(tmpdir)
            Execute(f'echo {self.__dir_structure}/{self.__amd_micro_name} | '
                    f'bsdcpio -o -H newc -R 0:0 >| {self.__amd_micro_boot}',
                    sh_wrap=True)


def main():
    parser = argparse.ArgumentParser()
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

    RootCheck(require_root=True)

    Microcode()
