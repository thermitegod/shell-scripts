# -*- coding: utf-8 -*-
# 6.8.0
# 2020-11-21

# Copyright (C) 2018,2019,2020 Brandon Zorn <brandonzorn@cock.li>
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
from python.utils.execute import Execute


class Ytdl:
    def __init__(self):
        self.__link = ''
        self.__audio_only = False

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

    def run(self, args):
        if args.audio:
            self.__audio_only = True

        self.__link = clipboard.from_flag_else_clipboard(args.url)

        net.link_check(self.__link)

        self.dl()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--audio',
                        action='store_true',
                        help='Only download audio')
    parser.add_argument('-u', "--url",
                        metavar='URL',
                        type=str,
                        nargs=1,
                        help='supply a video url, otherwise will get link from clipboard')
    args = parser.parse_args()

    utils.root_check(require_root=False)

    run = Ytdl()
    run.run(args)
