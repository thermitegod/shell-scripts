#!/usr/bin/env python3
# 2.0.0
# 2019-10-28

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
import shutil

from utils import utils


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--flexget',
                        action='store_true',
                        help='flexget')
    parser.add_argument('-y', '--youtube',
                        action='store_true',
                        help='youtube-dl')
    parser.add_argument('-o', '--other',
                        action='store_true',
                        help='random')
    args = parser.parse_args()

    utils.is_not_root()

    cache = os.path.join(os.environ.get('XDG_CACHE_HOME'), 'pip')

    pip = shutil.which('pip3')

    if not pip:
        pip = shutil.which('pip')

    cmd = pip + ' install --user --upgrade'

    if args.flexget:
        cmd += ' flexget'
    elif args.youtube:
        cmd += ' youtube-dl'
    elif args.other:
        cmd += ' PyGObject-stubs'
    else:
        exit('No requires flags enabled')

    utils.run_cmd(cmd)

    if os.path.exists(cache):
        shutil.rmtree(cache)


if __name__ == "__main__":
    main()
