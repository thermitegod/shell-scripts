# -*- coding: utf-8 -*-
# 2.4.0
# 2021-01-01

# Copyright (C) 2020,2021 Brandon Zorn <brandonzorn@cock.li>
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

from python.utils.check_env import CheckEnv
from python.utils.execute import Execute


class Initramfs:
    def __init__(self):
        self.__compression = None
        self.__kernel_version = None
        self.__no_firmware = False

    def gen_initramfs(self):
        cmd = '/usr/bin/dracut ' \
              '--hostonly ' \
              '--force ' \
              '--nofscks ' \
              f'--compress {self.__compression} ' \
              '-o "systemd systemd-initrd systemd-networkd" ' \
              '-o "lvmmerge btrfs dm dmraid dmsquash-live-ntfs lvm mdraid stratis cifs iscsi nfs" ' \
              '-o "modsign rngd network-legacy biosdevname masterkey bootchart" ' \
              '-o "crypt crypt-gpg" ' \
              '-o "i18n" '

        if self.__kernel_version:
            if 'rc' not in self.__kernel_version:
                if self.__kernel_version.endswith('-gentoo'):
                    cmd += f'--kver {self.__kernel_version} '
                else:
                    cmd += f'--kver {self.__kernel_version}-gentoo '
            else:
                cmd += f'--kver {self.__kernel_version} '

        if not self.__no_firmware:
            cmd += '-i /lib/firmware /lib/firmware '

        Execute(cmd)

    def run(self, args):
        if args.compression:
            self.__compression = args.compression[0]
        if args.kver:
            self.__kernel_version = args.kver[0]
        if args.no_firmware:
            self.__no_firmware = False

        self.gen_initramfs()


def main():
    parser = argparse.ArgumentParser()
    group1 = parser.add_argument_group('initramfs', 'control initramfs generation')
    group1.add_argument('-c', '--compression',
                        default='zstd',
                        type=str,
                        metavar='COMPRESSION',
                        choices=['zstd', 'lz4', 'lzo', 'xz'],
                        nargs=1,
                        help='compression algo used to compress initramfs [lz4]')
    group1.add_argument('-f', '--no-firmware',
                        action='store_true',
                        help='do not include firmware in initramfs')
    group1.add_argument('-k', '--kver',
                        default=None,
                        type=str,
                        nargs=1,
                        help='kernel version to gen initramfs for')
    args = parser.parse_args()

    CheckEnv.root_check(require_root=True)

    run = Initramfs()
    run.run(args)
