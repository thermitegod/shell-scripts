#!/usr/bin/env python3
# 9.5.0
# 2020-10-18

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
import os
from pathlib import Path

from utils import clipboard
from utils import dirs
from utils import editor
from utils import net
from utils import private
from utils import utils


class Download:
    def __init__(self):
        self.__user = private.mado_credentials(username=True)
        self.__pass = private.mado_credentials(password=True)
        self.__mode = utils.get_script_name()
        self.__extra = dirs.get_extra_dir()
        self.__link = ''
        self.__save_path = Path('/mnt/data')
        self.__symlink = True

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
        utils.run_cmd(cmd)
        print(f'downloaded: {self.__link}')
        print(f'save path:  {save_path_full}')

        if self.__symlink:
            if not Path.exists(save_path_full) and not Path.is_symlink(save_path_full):
                os.symlink(save_path_full, Path() / os.environ['HOME'] / 'media/manga-reading')

    def run(self, args):
        if self.__mode == 'madokami-novels-publishing':
            self.__extra = Path() / self.__extra / 'madokami-novels'
        elif self.__mode == 'madokami-manga-publishing':
            self.__extra = Path() / self.__extra / 'madokami-manga'

        if args.edit:
            editor.edit_conf(self.__extra)

        if args.save_dir:
            self.__save_path = Path() / self.__save_path / 'manga/neglected/finished'
        else:
            self.__save_path = Path() / self.__save_path / 'manga/neglected/in-print'

        if not args.symlink:
            self.__symlink = False

        if self.__mode == ('madokami-manga-publishing' or 'madokami-novels-publishing'):
            with Path.open(self.__extra) as fp:
                for link in fp:
                    self.__link = link
                    self.dl()
        else:
            self.__link = clipboard.from_flag_else_clipboard(args.url)

            self.dl()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--edit',
                        action='store_true',
                        help='Edit batch file')
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
    args = parser.parse_args()

    utils.root_check(require_root=False)

    run = Download()
    run.run(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
