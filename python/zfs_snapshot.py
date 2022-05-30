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
# 6.0.0
# 2021-05-06


import argparse
import sys
import time
from pathlib import Path

from loguru import logger

from utils.execute import Execute
from utils.root_check import RootCheck


class ZfsPools:
    def __init__(self, args=None):
        self.__selected_pool = None
        self.__cmd = 'zfs '

        self.parse_args(args=args)

    def parse_args(self, args):
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
        if args.list:
            self.__cmd += 'list -t snapshot '
            self.__selected_pool = args.list
        if args.snapshot:
            RootCheck(require_root=True)

            self.__cmd += 'snapshot '
            self.__selected_pool = args.snapshot

        if self.__selected_pool:
            if self.__selected_pool == '1':
                self.__cmd += 'zroot/ROOT/gentoo'
                if args.list:
                    # self.__cmd += ' zroot/ROOT/pkg'
                    self.__cmd += ' zroot/ROOT/gentoo/var'
            elif self.__selected_pool == '2':
                self.__cmd += 'zroot/HOME/brandon'
            elif self.__selected_pool == '3':
                self.__cmd += 'storage/anime'
            elif self.__selected_pool == '4':
                self.__cmd += 'storage/data'
            elif self.__selected_pool == '5':
                self.__cmd += 'ssd-mirror/KVM'
            elif self.__selected_pool == '6':
                self.__cmd += 'torrents'
            elif self.__selected_pool == '7':
                self.__cmd += 'zroot/CACHE/torrents'

            if args.snapshot:
                snapshot_time = time.strftime('%F-%H%M', time.localtime())
                self.__cmd += f'@manual-{snapshot_time}'

            Execute(self.__cmd)

        if args.export:
            RootCheck(require_root=True)

            Execute(f'zfs send {args.export} | zstd -T0 >| {Path.cwd()}/{Path(args.export).name}.zst',
                    sh_wrap=True)


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    general = parser.add_argument_group('general')
    general.add_argument('-B', '--export',
                         help='export passed snapshot')
    general.add_argument('-e', '--extra',
                         action='store_true',
                         help='Print extra info and exit')
    pools = parser.add_argument_group('valid pools',
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

    ZfsPools(args=args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
