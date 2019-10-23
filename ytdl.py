#!/usr/bin/env python3
# 5.0.0
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
import pyperclip


from utils import utils


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--audio',
                        action='store_true',
                        help='Only download audio')
    parser.add_argument('-u', "--url",
                        help='supply a video url, otherwise will get link from clipboard')
    group1 = parser.add_argument_group('Batch', 'NOT IMPLEMENTED')
    group1.add_argument('-b', '--batch',
                        action='store_true',
                        help='Download from batch file')
    group1.add_argument('-e', '--edit',
                        action='store_true',
                        help='edit batch file')
    group1.add_argument('-r', '--batch-rm',
                        action='store_true',
                        help='Delete batch file')
    args = parser.parse_args()

    utils.is_not_root()

    if args.batch:
        utils.not_implemented()

    if args.edit:
        utils.not_implemented()

    if args.batch_rm:
        utils.not_implemented()

    if args.url:
        link = args.url
    else:
        link = pyperclip.paste()

    if not link[:4] == 'http':
        exit('Invalid URL')

    print('downloading: ', link)

    cmd = 'youtube-dl --geo-bypass --no-overwrites --no-call-home --yes-playlist ' \
          '--audio-format best --audio-quality 0 --no-check-certificate'

    if args.audio:
        cmd += ' --extract-audio'

    cmd += ' ' + link

    utils.run_cmd(cmd)


if __name__ == "__main__":
    main()
