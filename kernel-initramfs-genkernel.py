#!/usr/bin/env python3
# 3.2.0
# 2019-10-23

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
import multiprocessing
import os
import os.path

from utils import utils


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--logfile',
                        action='store_true',
                        help='Gen logfile at /tmp/genkernel-initgen.log')
    parser.add_argument('-L', '--loglevel',
                        default=1,
                        type=int,
                        help='loglevel, valid range [0-5]')
    group1 = parser.add_argument_group('Initramfs', 'Control initramfs generation')
    group1.add_argument('-c', '--compression',
                        default='lz4',
                        type=str,
                        help='compression algo used to compress initramfs [lz4]')
    group1.add_argument('-e', '--encrypt',
                        action='store_true',
                        help='lvm ext4 encryption support')

    args = parser.parse_args()

    utils.is_root()

    if not os.path.isfile('/usr/src/linux/usr/gen_init_cpio'):
        exit('Make sure the kernel is build first')

    cmd = '/usr/bin/genkernel initramfs'
    cmd += f' --makeopts=-j{multiprocessing.cpu_count()}'
    cmd += ' --no-mdadm --no-nfs --no-dmraid --no-btrfs --no-multipath --no-iscsi --no-hyperv'
    cmd += ' --no-ssh --no-gpg --no-mountboot --no-unionfs --no-netboot --no-dmraid'
    cmd += ' --no-ramdisk-modules --busybox --no-keymap --postclear --disklabel'
    cmd += f' --compress-initramfs --compress-initramfs-type={args.compression}'
    cmd += ' --zfs'
    cmd += ' --microcode --firmware --firmware-dir=/lib/firmware'
    cmd += f' --loglevel={args.loglevel}'

    if args.encrypt:
        cmd += ' --lvm --luks --e2fsprogs'
    else:
        cmd += ' --no-lvm --no-luks --no-e2fsprogs'

    if args.logfile:
        cmd += ' --logfile=/tmp/genkernel-initgen.log'
    else:
        cmd += ' --logfile=/dev/null'

    utils.run_cmd(cmd)


if __name__ == "__main__":
    main()
