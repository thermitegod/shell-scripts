#!/usr/bin/env python3

# Copyright (C) 2018-2025 Brandon Zorn <brandonzorn@cock.li>
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
# 4.1.0
# 2025-10-29


# ZFS Builtin Kernel Build Script - gentoo

# recommended bootloader is ZFSBootMenu

# assumptions
# /usr/src/linux is real source or symlink to real source

# What this script does, basically

# runs configure phase on sys-fs/zfs ebuild
# installs configured zfs to /usr/src/linux
# builds kernel
# creates initramfs

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

from utils.execute import Execute
from utils.gentoo import GentooCheck
from utils.kernel import Kernel
from utils.root_check import RootCheck
from utils.script import ExecuteFishScript


# TODO
#   add comments for all niche cases in script


class Build:
    def __init__(self, args: argparse = None):
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
        self.__clean_kernel_src: bool = True

        self.__zfs_ebuild: Path = Path('sys-fs/zfs')
        self.__zfs_ebuild_path: Path = Path()
        self.__zfs_ebuild_revision: str
        self.__zfs_version: Path = Path()
        self.__zfs_version_path: Path = Path()

        self.__run_intro: bool = True
        self.__run_intro_extra: bool = False

        self.__run_zfs_checks: bool = True
        self.__run_zfs_build: bool = True

        self.__run_kernel_build: bool = True
        self.__run_kernel_post: bool = True
        self.__run_kernel_install: bool = True

        self.__run_emerge: bool = False

        self.parse_args(args=args)

        self.build()

    def intro(self):
        compiler = "Clang" if self.__cc_use_clang else "GCC"
        print(f'Kernel Source          : {self.__kernel_src}\n'
              f'Kernel Build           : {self.__run_kernel_build}\n'
              f'Kernel Install         : {self.__run_kernel_install}\n'
              f'Compiler               : {compiler}\n'
              f'ZFS version            : {self.__zfs_version}\n'
              f'ZFS ebuild repo        : {'local' if self.__use_zfs_local_ebuild else 'gentoo'}\n'
              f'ZFS rebuild userland   : {self.__run_zfs_build}\n'
              f'emerge @module-rebuild : {self.__run_emerge}')
        if self.__run_intro_extra:
            print(f'EXTRA\n'
                  f'Make command           : {self.run_compiler(return_only=True)}\n'
                  f'Tempdir                : {self.__tmpdir}\n'
                  f'Experimental opts      : {self.__experimental}')
            Execute('eselect kernel list')

        input('\nEnter to start kernel build ')

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

        kmake += f'chrt --idle 0 make -j{cores * 2 + 1} -l{cores + 1} CC={cc} LD={ld} {act}'
        if return_only:
            return kmake

        Execute(kmake, sh_wrap=True)

    def zfs_checks(self):
        repo_conf_dir = Path('/etc/portage/repos.conf')
        if not repo_conf_dir.is_dir():
            logger.error(f'must be a dir, {repo_conf_dir}')
            raise SystemExit

        repo_conf = 'gentoo.conf'
        if self.__use_zfs_local_ebuild:
            repo_conf = 'local.conf'

        repo_conf_full = Path() / repo_conf_dir / repo_conf
        if not repo_conf_full.is_file():
            logger.error(f'missing repo config file, {repo_conf_full}')
            raise SystemExit

        for line in Path.open(repo_conf_full):
            if 'location' in line:
                repo_path = line.split()[2]
                break

        if self.__use_zfs_release_version:
            emerge_out = Execute(f'emerge -pq sys-fs/zfs', to_stdout=True).get_out()

            # emerge output post processing
            # [16:] - removes '[ebuild   R   ] '
            ebuild = emerge_out[16:]
            # removes USE flags and current version text box,
            # [ebuild     U ] sys-fs/zfs-2.4.0_rc3 [2.3.4] USE="..."
            ebuild = ebuild.partition('USE=')[0].partition(' ')[0].strip()
            version = ebuild.removeprefix('sys-fs/zfs-')
            # remove any revision number for this ebuild
            if "-r" in version:
                self.__zfs_version = version.rpartition("-r")[0]
            else:
                self.__zfs_version = version
        else:
            # git
            self.__zfs_version = '9999'

        ebuild_revision_tags = ['', '-r1', '-r2', '-r3', '-r4', '-r5', '-r6', '-r7', '-r8', '-r9', '-r10']
        for revision in reversed(ebuild_revision_tags):
            self.__zfs_ebuild_path = Path() / repo_path / self.__zfs_ebuild / f'zfs-{self.__zfs_version}{revision}.ebuild'
            if Path.is_file(self.__zfs_ebuild_path):
                self.__zfs_ebuild_revision = revision
                break

        if not Path.is_file(self.__zfs_ebuild_path):
            logger.critical(f'missing ebuild \'{self.__zfs_ebuild_path}\'')
            raise SystemExit(1)

    def build_zfs(self):
        self.__zfs_version_path = self.__zfs_version

        if '_rc' in self.__zfs_version:
            # rc ebuilds
            self.__zfs_version = self.__zfs_version.replace('_', '-')
        elif '-r' in self.__zfs_version:
            # rev bump ebuilds
            self.__zfs_version = self.__zfs_version.rpartition('-')[0]

        self.cdkdir()
        self.msc()

        # Cheap workaround for the following portage kernel module check changes,
        # abridged error below. This is a false positive because ZFS will be built
        # into the kernel.
        #
        # '/usr/src/linux/Module.symvers' was not found implying that the
        # linux-6.3.5-gentoo tree at that location has not been built.
        #
        # Call stack:
        #              ebuild.sh, line 136:  Called pkg_setup
        #   zfs-kmod-9999.ebuild, line  92:  Called linux-mod-r1_pkg_setup
        #    linux-mod-r1.eclass, line 311:  Called _modules_prepare_kernel
        #    linux-mod-r1.eclass, line 631:  Called _modules_sanity_kernelbuilt
        #    linux-mod-r1.eclass, line 1029:  Called die
        # The specific snippet of code:
        #   		die "built kernel sources are required to build kernel modules"
        portage_check_module_symvers = Path() / self.__kernel_src / 'Module.symvers'
        portage_check_module_symvers_user_created = False
        if not portage_check_module_symvers.exists():
            portage_check_module_symvers_user_created = True
            Execute(f'touch {portage_check_module_symvers}')

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

        zfs_portage_build_path = Path() / self.__tmpdir / 'portage' / f'{self.__zfs_ebuild}-{self.__zfs_version_path}{self.__zfs_ebuild_revision}' / 'work' / f'zfs-{self.__zfs_version}'

        # Have to use ExecuteFishScript() because we use a custom portage tmpdir
        # using an env variable. Want the custom tmpdir because we only run the
        # configure phase for the zfs ebuild and I dont want to manualy remove it,
        # and the real tmpdir could also be in use.
        if self.__experimental:
            # zfs will configure and install into kernel source tree, the kernel build
            # will then fail with lots of errors.
            # the problem is the new ebuild does not use have a kernel-builtin
            # use flag that would set --with-config=kernel
            ExecuteFishScript(
                f'set -x PORTAGE_TMPDIR {self.__tmpdir}\n' \
                f'EXTRA_ECONF="--with-linux={self.__kernel_src} --enable-linux-builtin" ' \
                f'ebuild {self.__zfs_ebuild_path} configure ' \
                f'|| die "ebuild configure failed"\n')

            if not zfs_portage_build_path.exists():
                logger.critical(f'zfs build path missing: {zfs_portage_build_path}')
                raise SystemExit(1)
            os.chdir(zfs_portage_build_path)
        else:
            # run the configure phase manually to bypass configure flags set in the zfs ebuild.
            #
            # have to force gcc when runing configure to avoid this error
            # configure: error:
            #                 *** This kernel is unable to compile object files.
            #                 ***
            #                 *** Please make sure you prepared the Linux source tree
            #                 *** by running `make prepare` there.

            ExecuteFishScript(f'PORTAGE_TMPDIR={self.__tmpdir} ebuild {self.__zfs_ebuild_path} prepare')

            if not zfs_portage_build_path.exists():
                logger.critical(f'zfs build path missing: {zfs_portage_build_path}')
                raise SystemExit(1)
            os.chdir(zfs_portage_build_path)

            ExecuteFishScript(
                f'CC=gcc LD=ld.bfd ' \
                f'./configure --with-linux={self.__kernel_src} --enable-linux-builtin --with-config=kernel ' \
                f'|| die "configure failed"\n')

        Execute(f'./copy-builtin {self.__kernel_src}')

        if portage_check_module_symvers_user_created:
            # remove user created empty file Module.symvers
            Execute(f'rm {portage_check_module_symvers}')

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

            if self.__clean_kernel_src:
                self.run_compiler(act='distclean')

    def build(self):
        if not self.modules_check():
            logger.error(f'Missing module support')
            raise SystemExit(1)

        if self.__run_zfs_checks:
            self.zfs_checks()
        if self.__run_intro:
            self.intro()
        if self.__run_zfs_build:
            self.build_zfs()
        if self.__run_kernel_build:
            self.build_kernel()

    def parse_args(self, args):
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
        if args.compiler == 'clang':
            self.__cc_use_clang = True
        elif args.compiler == 'gcc':
            self.__cc_use_clang = False
        else:
            raise SystemExit(f'Unknown compiler {args.compiler}')
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
    ker.add_argument('-c', '--compiler',
                     default='clang',
                     metavar='COMPILER',
                     choices=['clang', 'gcc'],
                     help='set which compiler to build the kernel with, [%(choices)s], default [clang]')
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
                     help='disables post, emerge, and initramfs')
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
    GentooCheck()

    logger.remove()
    logger.add(sys.stdout, level=args.loglevel, colorize=True)

    Build(args=args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
