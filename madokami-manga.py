#!/usr/bin/env python3
# 8.0.0
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
import pyperclip


from utils import utils
from utils import private

save_path = '/mnt/data/'
save_path_full = None


def dl(link, symlink=False):
    global save_path_full
    if not link[:4] == 'http':
        print('not a valid url')
        return

    link_cut = link.split('/')[-1]
    save_path_full = f'{save_path}/{link_cut}'.replace('%20', ' ').replace('%21', '!')

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
          f'--directory-prefix={save_path} ' \
          f'--user {private.mado_user()} ' \
          f'--password {private.mado_pass()} ' \
          '--hsts-file=/tmp/wget-hsts ' \
          f'{link}'

    print('downloading: ', link)
    utils.run_cmd(cmd)
    print('downloaded: ', link)
    print('save path:  ', save_path_full)

    if symlink:
        if not os.path.exists(save_path_full) and not os.path.islink(save_path_full):
            os.symlink(save_path_full, os.path.join(os.environ.get('HOME'), 'media/manga-reading'))


def main():
    global save_path
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
                        help='supply a url, otherwise will get link from clipboard')
    args = parser.parse_args()

    utils.is_not_root()

    mode = utils.get_script_name()
    extra = utils.get_extra_dir()

    if mode == 'madokami-novels-publishing':
        extra += '/madokami-novels'
    else:
        extra += '/madokami-manga'

    if args.edit:
        utils.edit_conf(extra)

    if args.save_dir:
        save_path += 'manga/neglected/finished'
    else:
        save_path += 'manga/neglected/in-print'

    if args.symlink:
        symlink = True
    else:
        symlink = False

    if mode == 'madokami-manga-publishing' or mode == 'madokami-novels-publishing':
        with open(extra) as fp:
            for link in fp:
                dl(link, symlink)
    else:
        if args.url:
            link = args.url
        else:
            link = pyperclip.paste()

        dl(link, symlink)


if __name__ == "__main__":
    main()
