#!/usr/bin/env python3
# 5.0.0
# 2019-11-09

# Copyright (C) 2018,2019 Brandon Zorn <brandonzorn@cock.li>
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
from datetime import date

from utils import utils


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-l', '--list',
                        choices=['0', '1', '2', '3', '4', '5', '6', '7'],
                        # default=0,
                        help='0: all\n'
                             '1: zroot/ROOT/gentoo\n'
                             '2: zroot/HOME/brandon\n'
                             '3: storage/anime\n'
                             '4: storage/data\n'
                             '5: ssd-mirror/KVM\n'
                             '6: torrents\n'
                             '7: zroot/CACHE/torrents\n')
    parser.add_argument('-m', '--snapshot',
                        choices=['1', '2', '3', '4', '5', '6', '7'],
                        # default=1,
                        help='1: zroot/ROOT/gentoo\n'
                             '2: zroot/HOME/brandon\n'
                             '3: storage/anime\n'
                             '4: storage/data\n'
                             '5: ssd-mirror/KVM\n'
                             '6: torrents\n'
                             '7: zroot/CACHE/torrents\n')
    parser.add_argument('-B', '--export',
                        help='export passed snapshot')
    parser.add_argument('-e', '--extra',
                        action='store_true',
                        help='Print extra info and exit')
    args = parser.parse_args()

    if args.extra:
        print('zfs send pool/dataset@snapshot | zstd -T0 >| /tmp/backup.zst')
        print('unzstd -c backup.zst | zfs receive pool/newdataset')
        print('')
        print('zfs set mountpoint=/newmount pool/dataset')
        print('')
        print('zfs snapshot -r zroot/ROOT/gentoo@<type>-<date>')
        print('zfs rollback -r <pool/dataset@snapshot>')
        print('zfs destroy <pool/dataset@snapshot>')
        print('zfs list -t snapshot')
        print('zfs list -r pool')
        exit(0)

    if args.list:
        cmd = 'zfs list -t snapshot '

        if args.list == '1':
            cmd += 'zroot/ROOT/gentoo ' \
                   'zroot/ROOT/gentoo/var'
        elif args.list == '2':
            cmd += 'zroot/HOME/brandon'
        elif args.list == '3':
            cmd += 'storage/anime'
        elif args.list == '4':
            cmd += 'storage/data'
        elif args.list == '5':
            cmd += 'ssd-mirror/KVM'
        elif args.list == '6':
            cmd += 'torrents'
        elif args.list == '7':
            cmd += 'zroot/CACHE/torrents'

        utils.run_cmd(cmd)
        exit(0)

    if args.snapshot:
        utils.is_root()

        time = date.today()
        time = time.strftime('%F-%H%M')

        cmd = 'zfs snapshot -r '

        if args.snapshot == '1':
            cmd += 'zroot/ROOT/gentoo'
        elif args.snapshot == '2':
            cmd += 'zroot/HOME/brandon'
        elif args.snapshot == '3':
            cmd += 'storage/anime'
        elif args.snapshot == '4':
            cmd += 'storage/data'
        elif args.snapshot == '5':
            cmd += 'ssd-mirror/KVM'
        elif args.snapshot == '6':
            cmd += 'torrents'
        elif args.snapshot == '7':
            cmd += 'zroot/CACHE/torrents'
        else:
            exit('fallback hit')

        cmd += f'@{time}'
        utils.run_cmd(cmd)
        exit(0)

    if args.export:
        utils.is_root()
        target = args.export
        cmd = f'sh -c "zfs send {target} | zstd -T0 >| {os.path.basename(target)}.zst"'
        utils.run_cmd(cmd)
        exit(0)


if __name__ == '__main__':
    main()
