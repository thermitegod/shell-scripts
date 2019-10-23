#!/usr/bin/env python3
# 4.0.0
# 2019-10-24

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


import time
import os

from utils import utils


def main():
    cmd = 'gm import'

    if utils.get_script_name() == 'snip-root':
        cmd += ' -window root'

    cmd += f' {os.environ.get("HOME")}/{int(time.time())}.png'

    utils.run_cmd(cmd)


if __name__ == "__main__":
    main()
