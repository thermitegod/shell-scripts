#!/usr/bin/env python3

# Copyright (C) 2018-2022 Brandon Zorn <brandonzorn@cock.li>
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
# 6.11.0
# 2021-04-29


import argparse
import sys

from loguru import logger

from utils import clipboard
from utils import net
from utils.execute import Execute
from utils.root_check import RootCheck


class Ytdl:
    def __init__(self, args: argparse = None):
        self.__link = ''
        self.__audio_only = False

        self.parse_args(args=args)

        self.dl()

    def dl(self):
        cmd = 'youtube-dl ' \
              '--geo-bypass ' \
              '--no-overwrites ' \
              '--no-call-home ' \
              '--yes-playlist ' \
              '--format best ' \
              '--continue ' \
              '--ignore-errors ' \
              '--audio-format best ' \
              '--audio-quality 0 ' \
              '--no-check-certificate '

        if self.__audio_only:
            cmd += '--extract-audio '

        cmd += self.__link

        print(f'downloading: {self.__link}')
        Execute(cmd)
        print(f'downloaded: {self.__link}\n')

    def parse_args(self, args):
        if args.audio:
            self.__audio_only = True

        self.__link = clipboard.from_flag_else_clipboard(args.url)
        net.link_check(self.__link)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--audio',
                        action='store_true',
                        help='Only download audio')
    parser.add_argument('-u', '--url',
                        metavar='URL',
                        type=str,
                        nargs=1,
                        help='supply a video url, otherwise will get link from clipboard')
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

    RootCheck(require_root=False)

    Ytdl(args=args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
