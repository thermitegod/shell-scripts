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
# 10.6.0
# 2021-04-29


import argparse
import os
import sys
from pathlib import Path

from loguru import logger

from utils import clipboard
from utils import net
from utils.check_env import CheckEnv
from utils.execute import Execute
from utils.root_check import RootCheck

try:
    from private.manga_list import MangaList
except ImportError:
    print('Missing config file, see python/template/manga_list.py')
    raise SystemExit(1)

try:
    from private import mado_pass
except ImportError:
    print('Missing config file, see python/template/mado_pass.py')
    raise SystemExit(1)


class Download:
    def __init__(self, args: argparse = None):
        self.__user, self.__pass = mado_pass.mado_login()

        self.__mode = CheckEnv.get_script_name()
        self.__link = ''
        self.__save_path = Path('/mnt/data')
        self.__symlink = True

        self.parse_args(args=args)

    def dl(self):
        net.link_check(self.__link)

        link_cut = self.__link.split('/')[-1]
        save_path_full = Path() / self.__save_path / link_cut.replace('%20', ' ').replace('%21', '!')

        cmd = 'wget ' \
              '--random-wait ' \
              '--recursive ' \
              '--level=2 ' \
              '-e robots=off ' \
              '--no-parent ' \
              '--timestamping ' \
              '--max-redirect 0 ' \
              '--no-host-directories ' \
              '--cut-dirs=4 ' \
              '--accept zip,7z,rar,cbr,cbz,pdf,epub,mobi ' \
              f'--directory-prefix={self.__save_path} ' \
              f'--user {self.__user} ' \
              f'--password {self.__pass} ' \
              '--hsts-file=/tmp/wget-hsts ' \
              f'{self.__link}'

        print(f'downloading: {self.__link}')
        Execute(cmd)
        print(f'downloaded: {self.__link}')
        print(f'save path:  {save_path_full}')

        if self.__symlink:
            if not Path.exists(save_path_full) and not Path.is_symlink(save_path_full):
                os.symlink(save_path_full, Path() / os.environ['HOME'] / 'media/manga-reading')

    def parse_args(self, args):
        if args.save_dir:
            self.__save_path = Path() / self.__save_path / 'manga/neglected/finished'
        else:
            self.__save_path = Path() / self.__save_path / 'manga/neglected/in-print'

        if not args.symlink:
            self.__symlink = False

        if self.__mode == ('madokami-manga-publishing' or 'madokami-novels-publishing'):
            if self.__mode == 'madokami-manga-publishing':
                url_list = MangaList.MANGA_LIST
            else:
                url_list = MangaList.NOVEL_LIST

            for link in url_list:
                self.__link = link
                self.dl()
        else:
            self.__link = clipboard.from_flag_else_clipboard(args.url)
            self.dl()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--save-dir',
                        action='store_true',
                        help='Save to finished publishing dir')
    parser.add_argument('-l', '--symlink',
                        action='store_true',
                        help='symlink')
    parser.add_argument('-u', "--url",
                        metavar='URL',
                        type=str,
                        nargs=1,
                        help='supply a url, otherwise will get link from clipboard')
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

    Download(args=args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
