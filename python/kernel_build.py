# -*- coding: utf-8 -*-
# 3.0.0
# 2021-10-19

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

# ZFS Builtin Kernel Build Script - gentoo

# assumptions
# /usr/src/linux is real source or symlink to real source

# What this script does, basically

# runs configure phase on sys-fs/zfs-kmod ebuild
# installs configured kmod-zfs to /usr/src/linux
# builds kernel
# creates initramfs
# updates grub config

# required external scrips, must be in $PATH
#   kernel-clean-src
#   kernel-grub
#   kernel-initramfs

import argparse
import atexit
import multiprocessing
import os
import shutil
import sys
import tempfile
from pathlib import Path

from loguru import logger
from packaging import version

from python.utils.execute import Execute
from python.utils.kernel import Kernel
from python.utils.root_check import RootCheck
from python.utils.script import ExecuteScript


# TODO
#   add comments for all niche cases in script


class Build:
    def __init__(self, args: argparse = None):
        self.__MIN_KERNEL_VERSION: str = '4.17.0'
        self.__MIN_ZFS_VERSION: str = '2.1.0'

        atexit.register(self.remove_tmpdir)

        self.__tmpdir: Path = Path(tempfile.mkdtemp())
        # script is run as root but tmpdir needs to be rw for portage
        Path.chmod(self.__tmpdir, 0o777)

        self.__kernel_src: Path = Kernel.get_kernel_dir()
        self.__kernel_config: Path = Path() / self.__kernel_src / '.config'

        self.__kernel_vmlinux = self.__kernel_src / 'vmlinux'

        if not Path.is_file(self.__kernel_config):
            logger.critical('Kenrel directory is missing kernel config')
            raise SystemExit(1)

        self.__use_zfs_release_version: bool = True
        self.__use_zfs_local_ebuild: bool = False

        self.__cc_use_clang: bool = True
        self.__experimental: bool = False
        self.__gentoo_repo_path: Path = Path()
        self.__clean_kernel_src: bool = True

        self.__zfs_ebuild: Path = Path('sys-fs/zfs-kmod')
        self.__zfs_ebuild_path: Path = Path()
        self.__zfs_version: Path = Path()
        self.__zfs_version_path: Path = Path()
        self.__zfs_kmod_build_path: Path = Path()

        self.__run_intro: bool = True
        self.__run_intro_extra: bool = False

        self.__run_zfs_checks: bool = True
        self.__run_zfs_build: bool = True

        self.__run_kernel_build: bool = True
        self.__run_kernel_post: bool = True
        self.__run_kernel_install: bool = True

        self.__run_emerge: bool = False

        self.__initramfs_compression: str = 'zstd'

        # gets module version for 'dracut -k' and versioned storage path for saved work
        self.__kernel_module_dir = self.__kernel_src.name[6:]
        if 'rc' in self.__kernel_module_dir:
            # release candidate

            # fun shit
            # modules naming scheme is x.x.x-rcx but gentoo naming is x.x-rcx
            # i.e. 5.7-rc1 -> 5.7.0-rc1
            kver_tmp = self.__kernel_module_dir.rpartition('-')
            self.__kernel_module_dir = f'{kver_tmp[0]}.0{kver_tmp[1]}{kver_tmp[2]}'

        self.version_check_kernel(ver=self.__kernel_module_dir.partition('-')[0])

        self.run(args=args)

    def intro(self):
        print(f'kernel             : {self.__kernel_src}\n'
              f'Using LLVM/Clang   : {self.__cc_use_clang}\n'
              f'Install            : {self.__run_kernel_install}\n'
              f'ZFS version        : {self.__zfs_version}\n'
              f'ZFS local ebuild   : {self.__use_zfs_local_ebuild}\n'
              f'ZFS build          : {self.__run_zfs_build}\n'
              f'Running emerge     : {self.__run_emerge}')
        if self.__run_intro_extra:
            print(f'EXTRA\n'
                  f'Min kernel version : {self.__MIN_KERNEL_VERSION}\n'
                  f'Min ZFS version    : {self.__MIN_ZFS_VERSION}\n'
                  f'Make command       : {self.run_compiler(return_only=True)}\n'
                  f'PORTDIR            : {self.__gentoo_repo_path}\n'
                  f'kernel module dir  : /lib/modules/{self.__kernel_module_dir}\n'
                  f'Tempdir            : {self.__tmpdir}\n'
                  f'Experimental opts  : {self.__experimental}')
            Execute('eselect kernel list')

        input('\nEnter to start kernel build ')

    def version_check_kernel(self, ver):
        required = self.__MIN_KERNEL_VERSION

        if version.parse(required) > version.parse(ver):
            logger.critical(f'Minimum supported kernel version is: {required}, using {ver}')
            raise SystemExit(1)

    def version_check_zfs(self, ver):
        required = self.__MIN_ZFS_VERSION

        if version.parse(required) > version.parse(ver):
            logger.critical(f'Minimum supported zfs version is: {required}, using {ver}')
            raise SystemExit(1)

    def cdkdir(self):
        os.chdir(self.__kernel_src)

    def msc(self):
        self.run_compiler(act='syncconfig')

    def remove_tmpdir(self):
        shutil.rmtree(self.__tmpdir)

    def modules_check(self):
        for line in Path.open(self.__kernel_config):
            if 'CONFIG_MODULES=y' in line:
                return True
        return False

    def init_compression_check(self):
        for line in Path.open(self.__kernel_config):
            match line.strip():
                case 'CONFIG_RD_ZSTD=y':
                    self.__initramfs_compression = 'zstd'
                    return True
                case 'CONFIG_RD_LZ4=y':
                    self.__initramfs_compression = 'lz4'
                    return True
                case 'CONFIG_RD_LZO=y':
                    self.__initramfs_compression = 'lzo'
                    return True
                case 'CONFIG_RD_XZ=y':
                    self.__initramfs_compression = 'xz'
                    return True
        return False

    def run_compiler(self, act='', force_gcc=False, return_only=False):
        # keep CC/LD to override env, probably not needed though
        cores = multiprocessing.cpu_count()
        cc = ''
        ld = ''
        kmake = ''
        if not self.__cc_use_clang or force_gcc:
            # gcc
            cc = 'gcc'
            ld = 'ld.bfd'
        elif self.__cc_use_clang:
            # clang
            cc = 'clang'
            ld = 'ld.lld'
            kmake += f'LLVM=1 LLVM_IAS=1 '
            # if self.__experimental:
            #     kmake += 'LLVM_IAS=1 '

        kmake += f'nice -19 make -j{cores * 2 + 1} -l{cores + 1} CC={cc} LD={ld} {act}'
        if return_only:
            return kmake

        Execute(kmake, sh_wrap=True)

    def zfs_checks(self):
        repo_conf_dir = Path('/etc/portage/repos.conf')
        if not repo_conf_dir.is_dir():
            logger.error(f'must be a dir, {repo_conf_dir}')
            raise SystemExit

        if self.__use_zfs_local_ebuild:
            repo_conf = 'local.conf'
        else:
            repo_conf = 'gentoo.conf'

        repo_conf_full = Path() / repo_conf_dir / repo_conf
        if not repo_conf_full.is_file():
            logger.error(f'missing repo config file, {repo_conf_full}')
            raise SystemExit

        for line in Path.open(repo_conf_full):
            if 'location' in line:
                self.__gentoo_repo_path = line.split()[2]
                break

        if self.__use_zfs_release_version:
            wanted_ebuild = None
            zfs_ebuild_path = Path() / self.__gentoo_repo_path / self.__zfs_ebuild
            for ebuild in Path(zfs_ebuild_path).iterdir():
                ebuild = str(ebuild)
                if ebuild.endswith('.ebuild') and not ebuild.endswith('9999.ebuild'):
                    wanted_ebuild = ebuild

            self.__zfs_version = wanted_ebuild.rpartition('.')[0].rpartition('/')[-1][9:]

            # build path
            self.__zfs_kmod_build_path = "zfs"
            self.version_check_zfs(ver=self.__zfs_version)
        else:
            # git
            self.__zfs_version = '9999'
            # build path
            self.__zfs_kmod_build_path = 'zfs-kmod'

        self.__zfs_ebuild_path = Path() / self.__gentoo_repo_path / self.__zfs_ebuild / f'zfs-kmod-{self.__zfs_version}.ebuild'
        if not Path.is_file(self.__zfs_ebuild_path):
            logger.critical(f'missing ebuild \'{self.__zfs_ebuild_path}\'')
            raise SystemExit(1)

    def build_zfs(self):
        self.__zfs_version_path = self.__zfs_version

        if 'rc' in self.__zfs_version:
            # rc ebuilds
            self.__zfs_version = self.__zfs_version.rpartition('_')[0]
        if '-r' in self.__zfs_version:
            # rev bump ebuilds
            self.__zfs_version = self.__zfs_version.rpartition('-')[0]

        self.build_zfs_clean_build()

    def build_zfs_clean_build(self):
        self.cdkdir()
        self.msc()

        if not self.__experimental:
            # get error when running zfs configure
            # 	*** Unable to build an empty module.
            # 	*** Please run 'make scripts' inside the kernel source tree.
            # running 'make scripts' does not fix the problem
            # using gcc does fix the problem
            # backup .config before GCC removes clang specific CONFIG_*
            Kernel.kernel_conf_copy(src=self.__kernel_src, dst=self.__tmpdir)
            self.run_compiler(act='prepare', force_gcc=True)
        else:
            self.run_compiler(act='prepare')

        portage_env = f'export PORTAGE_TMPDIR="{self.__tmpdir}"\n'

        zfs_build_path = Path() / self.__tmpdir / 'portage' / f'{self.__zfs_ebuild}-{self.__zfs_version_path}' / 'work'
        zfs_build_version = f'{self.__zfs_kmod_build_path}-{self.__zfs_version}'

        # this is just simpler
        text = f'{portage_env}\n' \
               f'EXTRA_ECONF="--with-linux={self.__kernel_src} --enable-linux-builtin" ebuild ' \
               f'{self.__zfs_ebuild_path} configure || die "build failed"\n'
        ExecuteScript(text)

        os.chdir(Path() / zfs_build_path / zfs_build_version)
        Execute(f'./copy-builtin {self.__kernel_src}')

        if not self.__experimental:
            # Since GCC is used to to configure, any clang specific
            # kernel options are lost. Restore config that has these options
            Kernel.kernel_conf_copy(src=self.__tmpdir, dst=self.__kernel_src)

        if self.__cc_use_clang:
            # when using clang to run 'make prepare' get error when running zfs configure
            # 'Unable to build an empty module.'
            # so clean kernel src since gcc was used in prepare
            Execute('kernel-clean-src -c')

    def build_kernel(self):
        self.cdkdir()
        self.msc()

        for idx, item in enumerate(range(4)):
            if idx == 3:
                # only try 3 time otherwise something else is wrong
                logger.critical('Multiple build failures, exiting')
                raise SystemExit(1)

            self.run_compiler()

            if Path.is_file(self.__kernel_vmlinux):
                # deal with an llvm compile bug where the build will fail
                # but just running 'make' again will finish the build
                break
            else:
                logger.warning('build failure, resuming build')

        if not Path.is_file(self.__kernel_vmlinux):
            # extra guard, not really needed
            logger.critical('missing vmlinux, exiting')
            raise SystemExit(1)

        if self.__run_kernel_install:
            self.run_compiler(act='modules_install')
            self.run_compiler(act='install')

        if self.__run_kernel_post:
            if self.__run_emerge:
                if self.__run_zfs_build:
                    if self.__use_zfs_release_version:
                        Execute('emerge --ignore-default-opts --oneshot --quiet --update sys-fs/zfs')
                    else:
                        # will always rebuild zfs when using git
                        Execute('emerge --ignore-default-opts --oneshot --quiet sys-fs/zfs')
                Execute('emerge --ignore-default-opts --oneshot --jobs @module-rebuild')
            Execute(f'kernel-initramfs -c {self.__initramfs_compression} -k {self.__kernel_module_dir}')
            Execute('kernel-grub')
            if self.__clean_kernel_src:
                Execute('kernel-clean-src -c')

    def build(self):
        if not self.modules_check():
            logger.error(f'Missing module support')
            raise SystemExit(1)

        if not self.init_compression_check():
            logger.error(f'Unable to get initramfs compression')
            raise SystemExit(1)
        logger.debug(f'initramfs compression: {self.__initramfs_compression}')

        if self.__run_zfs_checks:
            self.zfs_checks()
        if self.__run_intro:
            self.intro()
        if self.__run_zfs_build:
            self.build_zfs()
        if self.__run_kernel_build:
            self.build_kernel()

    def run(self, args):
        # General
        if args.no_intro:
            self.__run_intro = False
        if args.verbose:
            self.__run_intro_extra = True
        # ZFS
        if args.use_git:
            self.__use_zfs_release_version = False
        if args.use_release:
            self.__use_zfs_release_version = True
        if args.use_local_ebuild:
            self.__use_zfs_local_ebuild = True
        # Kernel
        if args.compiler:
            self.__cc_use_clang = False
        if args.no_clean:
            self.__clean_kernel_src = False
        if args.emerge:
            self.__run_emerge = True
        if args.no_install:
            self.__run_kernel_post = False
            self.__run_kernel_install = False
        if args.no_post:
            self.__run_kernel_post = True
        if args.fancy_make:
            self.__run_zfs_checks = False
            self.__run_zfs_build = False
        if args.zfs_install:
            self.__run_zfs_build = True
            self.__run_kernel_build = False
        if args.experimental:
            self.__experimental = True

        self.build()


def main():
    parser = argparse.ArgumentParser()
    general = parser.add_argument_group('general')
    general.add_argument('-I', '--no-intro',
                         action='store_true',
                         help='disable intro')
    general.add_argument('-v', '--verbose',
                         action='store_true',
                         help='set verbose on')
    zfs = parser.add_argument_group('zfs')
    zfs.add_argument('-g', '--use-git',
                     action='store_true',
                     help='use git ebuild')
    zfs.add_argument('-r', '--use-release',
                     action='store_true',
                     help='use release ebuild')
    zfs.add_argument('-l', '--use-local-ebuild',
                     action='store_true',
                     help='use local repo in $PORTDIR_OVERLAY')
    ker = parser.add_argument_group('kernel')
    ker.add_argument('-G', '--compiler',
                     action='store_true',
                     help='build kernel using gcc')
    ker.add_argument('-C', '--no-clean',
                     action='store_true',
                     help='disable cleaning kernel source dir')
    ker.add_argument('-e', '--emerge',
                     action='store_true',
                     help='enable running emerge in post')
    ker.add_argument('-i', '--no-install',
                     action='store_true',
                     help='build kernel but do not install or run post, implies -p')
    ker.add_argument('-p', '--no-post',
                     action='store_true',
                     help='disable post, emerge, initramfs, and grub configure')
    ker.add_argument('-x', '--fancy-make',
                     action='store_true',
                     help='disable zfs build, becomes fancy \'make;make install\'')
    ker.add_argument('-z', '--zfs-install',
                     action='store_true',
                     help='only run zfs build, will install zfs into kenrel tree')
    ker.add_argument('-Z', '--experimental',
                     action='store_true',
                     help='enables experimental options, may or may not do something, or even work')
    debug = parser.add_argument_group('debug')
    debug.add_argument('-L', '--loglevel',
                       default='INFO',
                       metavar='LEVEL',
                       type=str.upper,
                       choices=['NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'VERBOSE', 'DEBUG', 'TRACE'],
                       help='Levels: %(choices)s')
    args = parser.parse_args()

    RootCheck(require_root=True)

    logger.remove()
    logger.add(sys.stdout, level=args.loglevel, colorize=True)

    Build(args=args)
