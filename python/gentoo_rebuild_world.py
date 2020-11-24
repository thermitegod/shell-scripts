# -*- coding: utf-8 -*-
# 1.3.0
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
from pathlib import Path

from python.utils import utils
from python.utils.execute import Execute


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--rebuild-gcc',
                        action='store_true',
                        help='rebuils all pkgs build with gcc')
    parser.add_argument('-c', '--rebuild-clang',
                        action='store_true',
                        help='rebuils all pkgs build with clang')
    args = parser.parse_args()

    utils.root_check(require_root=True)

    env = Path() / '/etc/portage/package.env'
    gcc_req_ebuilds = ''
    for pkg in Path.open(env):
        if 'cc-gcc' in pkg:
            pkg = pkg.split(' ')[0]
            if '#' not in pkg:
                gcc_req_ebuilds += f'{pkg} '

    if args.rebuild_clang:
        bin_pkg = 'www-client/google-chrome-unstable ' \
                  'dev-util/clion ' \
                  'dev-util/pycharm-community ' \
                  'dev-java/openjdk-bin ' \
                  'sys-kernel/gentoo-sources ' \
                  'sys-kernel/git-sources ' \
                  'sys-kernel/linux-firmware ' \
                  'media-fonts/noto ' \
                  'media-fonts/noto-cjk ' \
                  'media-fonts/liberation-fonts'
        virtual = 'virtual/*'
        user_group = 'acct-group/* acct-user/*'
        Execute('emerge --jobs --oneshot --emptytree @world '
                f'--exclude \'{gcc_req_ebuilds}\' '
                f'--exclude \'{virtual}\' '
                f'--exclude \'{user_group}\' '
                f'--exclude \'{bin_pkg}\'')

    if args.rebuild_gcc:
        Execute(f'emerge --jobs --oneshot {gcc_req_ebuilds}')