#!/usr/bin/env python3

# Copyright (C) 2018-2023 Brandon Zorn <brandonzorn@cock.li>
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
# 2.4.0
# 2023-01-06


import argparse
import sys
from pathlib import Path

from loguru import logger

from utils.execute import Execute
from utils.root_check import RootCheck


class Rebuild:
    def __init__(self, args=None):
        env = Path('/etc/portage/package.env')

        self.__gcc_req_ebuilds = ''
        for pkg in Path.open(env):
            if 'cc-gcc' in pkg:
                pkg = pkg.split(' ')[0]
                if '#' not in pkg:
                    self.__gcc_req_ebuilds += f'{pkg} '

        self.parse_args(args=args)

    def parse_args(self, args):
        if args.rebuild_clang:
            self.rebuild_clang()
        if args.rebuild_gcc:
            self.rebuild_gcc()

    def rebuild_clang(self):
        bin_pkg = 'www-client/google-chrome ' \
                  'www-client/google-chrome-beta ' \
                  'www-client/google-chrome-unstable ' \
                  'dev-lang/rust-bin ' \
                  'app-editors/vscode ' \
                  'sys-kernel/gentoo-sources ' \
                  'sys-kernel/git-sources ' \
                  'sys-kernel/linux-firmware ' \
                  'media-fonts/noto ' \
                  'media-fonts/noto-cjk ' \
                  'media-fonts/noto-emoji ' \
                  'media-fonts/liberation-fonts'
        virtual = 'virtual/*'
        user_group = 'acct-group/* acct-user/*'
        sec_keys = 'sec-keys/*'
        gcc = "sys-devel/gcc"
        Execute('emerge --jobs --oneshot --emptytree @world '
                f'--exclude \'{self.__gcc_req_ebuilds}\' '
                f'--exclude \'{virtual}\' '
                f'--exclude \'{user_group}\' '
                f'--exclude \'{sec_keys}\' '
                f'--exclude \'{gcc}\' '
                f'--exclude \'{bin_pkg}\' ')

    def rebuild_gcc(self):
        Execute(f'emerge --jobs --oneshot {self.__gcc_req_ebuilds}')


def main():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required exclusive arguments').add_mutually_exclusive_group(required=True)
    required.add_argument('-g', '--rebuild-gcc',
                          action='store_true',
                          help='rebuils all pkgs build with gcc')
    required.add_argument('-c', '--rebuild-clang',
                          action='store_true',
                          help='rebuils all pkgs build with clang')
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

    Rebuild(args=args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
