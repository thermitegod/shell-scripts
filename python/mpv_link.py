# -*- coding: utf-8 -*-
# 1.3.0
# 2020-11-11

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

from python.utils import clipboard
from python.utils import net
from python.utils import utils


class Mpv:
    def __init__(self):
        self.__link = None

    def run(self, args):
        self.__link = clipboard.from_flag_else_clipboard(args.url)

        net.link_check(self.__link)
        utils.run_cmd(f'mpv {self.__link}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', "--url",
                        metavar='URL',
                        type=str,
                        nargs=1,
                        help='supply a video url, otherwise will get link from clipboard')
    args = parser.parse_args()

    run = Mpv()
    run.run(args)
