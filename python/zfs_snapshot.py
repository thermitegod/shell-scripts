# -*- coding: utf-8 -*-
# 5.9.0
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
import time
from pathlib import Path

from python.utils import utils
from python.utils.execute import Execute


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    general = parser.add_argument_group('GENERAL')
    general.add_argument('-B', '--export',
                         help='export passed snapshot')
    general.add_argument('-e', '--extra',
                         action='store_true',
                         help='Print extra info and exit')
    pools = parser.add_argument_group('Valid pools',
                                      '0: all [list only]\n'
                                      '1: zroot/ROOT/gentoo [list adds /var/{db/pkg}]\n'
                                      '2: zroot/HOME/brandon\n'
                                      '3: storage/anime\n'
                                      '4: storage/data\n'
                                      '5: ssd-mirror/KVM\n'
                                      '6: torrents\n'
                                      '7: zroot/CACHE/torrents\n')
    pools.add_argument('-l', '--list',
                       metavar='POOLS',
                       choices=['0', '1', '2', '3', '4', '5', '6', '7'])
    pools.add_argument('-m', '--snapshot',
                       metavar='POOLS',
                       choices=['1', '2', '3', '4', '5', '6', '7'])
    args = parser.parse_args()

    if args.extra:
        print('zfs send pool/dataset@snapshot | zstd -T0 >| /tmp/backup.zst\n'
              'unzstd -c backup.zst | zfs receive pool/newdataset\n'
              '\n'
              'zfs set mountpoint=/newmount pool/dataset\n'
              '\n'
              'zfs snapshot -r zroot/ROOT/gentoo@<type>-<date>\n'
              'zfs rollback -r <pool/dataset@snapshot>\n'
              'zfs destroy <pool/dataset@snapshot>\n'
              'zfs list -t snapshot\n'
              'zfs list -r pool')
        raise SystemExit

    selected_pool = None
    cmd = 'zfs '

    if args.list:
        cmd += 'list -t snapshot '
        selected_pool = args.list

    if args.snapshot:
        utils.root_check(require_root=True)
        cmd += 'snapshot '
        selected_pool = args.snapshot

    if selected_pool:
        if selected_pool == '1':
            cmd += 'zroot/ROOT/gentoo'
            if args.list:
                cmd += ' zroot/ROOT/pkg'
                cmd += ' zroot/ROOT/gentoo/var'
        elif selected_pool == '2':
            cmd += 'zroot/HOME/brandon'
        elif selected_pool == '3':
            cmd += 'storage/anime'
        elif selected_pool == '4':
            cmd += 'storage/data'
        elif selected_pool == '5':
            cmd += 'ssd-mirror/KVM'
        elif selected_pool == '6':
            cmd += 'torrents'
        elif selected_pool == '7':
            cmd += 'zroot/CACHE/torrents'

        if args.snapshot:
            snapshot_time = time.strftime('%F-%H%M', time.localtime())
            cmd += f'@manual-{snapshot_time}'
        Execute(cmd)

    if args.export:
        utils.root_check(require_root=True)
        target = args.export
        Execute(f'zfs send {target} | zstd -T0 >| {Path.cwd()}/{Path(target).name}.zst',
                sh_wrap=True)