#!/usr/bin/env python3
# 6.2.0
# 2019-10-23

# Copyright (C) 2018,2019 Brandon Zorn, brandonzorn@cock.li
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
import os.path

from utils import utils


def main():
    parser = argparse.ArgumentParser()
    group1 = parser.add_argument_group('PROFILES')
    group1.add_argument('-d', '--default',
                        action='store_true',
                        help='default profile')
    group1.add_argument('-e', '--extra',
                        default='none',
                        type=str,
                        help='extra profiles, supplied arg is used as profile name')
    group1.add_argument('-s', '--sandbox',
                        action='store_true',
                        help='sandbox, all data deleted on close')
    group2 = parser.add_argument_group('BROWSER', 'which browser version to use')
    group2.add_argument('-c', '--chromium',
                        action='store_true',
                        help='chromium')
    group2.add_argument('-g', '--google-chrome',
                        default='unstable',
                        type=str,
                        help='chrome, valid are [unstable,beta,release]')
    args = parser.parse_args()

    utils.is_not_root()

    if args.chromium:
        cmd = 'chromium'
    elif args.google_chrome == 'unstable':
        cmd = 'google-chrome-unstable'
    elif args.google_chrome == 'beta':
        cmd = 'google-chrome-beta'
    else:
        cmd = 'google-chrome'

    profile = os.path.join(os.environ['HOME'], '.config/chrome')

    if args.extra is not 'none':
        profile_append = f'{cmd}-{args.extra}'
    else:
        # script/symlinks must be named chromium-<profile name> to work
        # or this can be changed
        profile_append = f'{cmd}-{utils.get_script_name()[9:]}'

    if args.sandbox:
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmpdir:
            cmd += f' --user-data-dir={tmpdir}'
            utils.run_cmd(cmd)
    else:
        profile += f'/{profile_append}'
        cmd += f' --user-data-dir={profile}'
        utils.run_cmd(cmd)


if __name__ == "__main__":
    main()
