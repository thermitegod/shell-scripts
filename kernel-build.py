#!/usr/bin/env python3
# 1.0.0
# 2019-02-28

# Copyright (C) 2020 Brandon Zorn <brandonzorn@cock.li>
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

# hard requirments
# >=linux-4.17.0 : >=zfs-0.8.0 / git | 1.x.x script for previous support

# storage dirs - need to exist
# ${XDG_DATA_DIRS}/kernel/{config,distfiles,src}

# assumptions
# /usr/src/linux is real source or symlink to real source
# $run_kernel_bump is based om my own config and others CONFIG_* options may be needed based on kenrel config

# What this script does, basically

# if no preconfigured sources exist for ebuild sys-fs/zfs-kmod
# runs configure phase on sys-fs/zfs-kmod ebuild
# saves work/ to tar.zst file in $kmod_src
# installs configured kmod-zfs to /usr/src/linux
# build kernel

# if preconfigured sources exist for ebuild sys-fs/zfs-kmod
# moves saved work in tar.zst file to /usr/src/linux
# build kernel

import argparse
import os
import shutil
import tempfile
import multiprocessing
import atexit
import pathlib

from utils import utils
from utils import kernel


# TODO
#   config file
#   add comments for all niche cases in script
#   multi build kernels
#       multi kernel build - debug and regular, from one invocation
#       single build, either debug or regular

class Build:
    def __init__(self):
        atexit.register(self.remove_tmpdir)

        self.__tmpdir = tempfile.mkdtemp()
        os.chmod(f'{self.__tmpdir}', 0o777)

        self.__ksym = kernel.get_kernel_dir()
        self.__kdir = os.path.realpath(self.__ksym)
        self.__kconf = f'{self.__kdir}/.config'

        self.__use_zfs_version = 'release'

        self.__use_local_zfs_ebuild = False

        self.__run_kernel_bump = False

        self.__cc_use_clang = False
        self.__cc = None
        self.__ld = None
        self.__kmake = None

        self.__kver_full = None
        self.__kver = None
        self.__repos = None
        self.__zfs_ebuild = None
        self.__zver = None
        self.__kmod = None
        self.__port = None
        self.__zfs_ebuild_full = None
        self.__kmod_src = None

        self.__clean_kernel_src = True

        self.__run_emerge = False
        self.__run_kmod_build = False

        self.__run_intro = True
        self.__run_zfs_build = True
        self.__run_zfs_checks = True
        self.__run_kernel_post = True
        self.__run_kernel_build = True
        self.__run_kernel_install = True

        self.__use_distdir = False

        self.__intro_extra = False
        self.__force_bump_check = False

        self.__use_modules = False
        self.__use_local_zfs_ebuild = False

        self.__storage = os.path.join(os.environ['XDG_DATA_HOME'], 'kernel')
        self.__settings = os.path.join(os.environ['XDG_CONFIG_HOME'], 'kernel/config')

        if not os.path.isdir(self.__storage):
            os.mkdir(self.__storage)

        if not os.path.isdir(f'{self.__storage}/distfiles'):
            os.mkdir(f'{self.__storage}/distfiles')

        if not os.path.isdir(f'{self.__storage}/src'):
            os.mkdir(f'{self.__storage}/src')

        if not os.path.isdir(f'{self.__storage}/config'):
            os.mkdir(f'{self.__storage}/config')

        self.__switch_kconf = f'{self.__storage}/config/{self.__kver}-config'
        if not os.path.isfile(self.__switch_kconf):
            self.__force_bump_check = True

    def intro(self):
        print(f'kernel             : {self.__kdir}')
        print(f'compiler/linker    : {self.set_compiler(get_cc=True)}')
        print(f'Install            : {self.__run_kernel_install}')
        print(f'ZFS version        : {self.__zver}')
        print(f'ZFS local ebuild   : {self.__use_local_zfs_ebuild}')
        print(f'Configure kmod     : {self.__run_kmod_build}')
        print(f'Enable modules     : {self.__use_modules}')
        print(f'Running emerge     : {self.__run_emerge}')
        if self.__intro_extra:
            print(f'EXTRA')
            print(f'Make command       : {self.__kmake}')
            print(f'PORTDIR            : {self.__repos}')
            print(f'kver               : {self.__kver}')
            print(f'kver_full          : {self.__kver_full}')
            print(f'Tempdir            : {self.__tmpdir}')
            utils.run_cmd('eselect kernel list')
        print()
        try:
            input('Enter to start kernel build ')
        except KeyboardInterrupt:
            exit()

    def cdkdir(self):
        os.chdir(self.__kdir)

    def cdtmp(self):
        os.chdir(self.__tmpdir)

    def msc(self):
        utils.run_cmd(f'{self.__kmake} syncconfig')

    def remove_tmpdir(self):
        shutil.rmtree(self.__tmpdir)

    def modules_check(self):
        if not self.__use_modules:
            for line in open(self.__kconf):
                if 'CONFIG_MODULES=y' in line:
                    self.__use_modules = True

    def set_compiler(self, get_cc=False):
        if self.__cc_use_clang:
            # ld.lld only works when clang is the compiler otherwise fails with
            # error: init sections too big!
            self.__cc = 'clang'
            self.__ld = 'ld.lld'
        else:
            # force bfd since gold is not supported
            # https://bugs.gentoo.org/694612
            # https://bugzilla.kernel.org/show_bug.cgi?id=204951
            self.__cc = 'gcc'
            self.__ld = 'ld.bfd'

        if get_cc:
            return self.__cc, self.__ld

        cores = multiprocessing.cpu_count()
        self.__kmake = f'nice -19 make -j{cores * 2 + 1} -l{cores + 1} CC={self.__cc} LD={self.__ld}'

    def kernel_bump(self):
        # CONFIG_MODULES and CONFIG_KALLSYMS are required to build kmod
        # which are not needed at runtime if zfs is build into the kernel.
        c1, c2, c3 = False, False, False
        while True:
            for line in open(self.__kconf):
                if 'CONFIG_MODULES=y' in line:
                    c1 = True
                if 'CONFIG_TRIM_UNUSED_KSYMS=y' in line:
                    c2 = False
                if 'CONFIG_KALLSYMS=y' in line:
                    c3 = True

            if not (c1 or c2 or c3):
                print('\nRequired option[s] located at:\n')
                if not c1:
                    print('\n[*] Enable loadable module support\n')
                if not c2:
                    print('\n[*] Enable loadable module support\n')
                    print('\t[ ]   Enable unused/obsolete exported symbols')
                    print('\t\t[ ]     Trim unused exported kernel symbols')
                if not c3:
                    print('\nGeneral setup  --->\n')
                    print('\t[*] Configure standard kernel features (expert users)  --->\n')
                    print('\t\t[*] Load all symbols for debugging/ksymoops\n\n')

                try:
                    input('Enter to config switch config: ')
                except KeyboardInterrupt:
                    exit()
                if os.path.isfile(self.__switch_kconf):
                    os.remove(self.__switch_kconf)
                self.cdkdir()
                utils.run_cmd(f'{self.__kmake} nconfig')
                shutil.copyfile(f'{self.__kdir}/.config', self.__switch_kconf)
            else:
                break

    def run_zfs_checks(self):
        self.__kver_full = os.path.basename(self.__kdir)
        if 'rc' in self.__kver_full:
            self.__kver = self.__kver_full.rpartition('_')[0]
        else:
            self.__kver = self.__kver_full.rpartition('.')[0]

        if self.__use_local_zfs_ebuild:
            repo_conf = 'gentoo.conf'
        else:
            repo_conf = 'local.conf'
        self.__repos = f'/etc/portage/repos.conf/{repo_conf}'
        for line in open(self.__repos):
            if 'location' in line:
                self.__port = line.split()[2]
                break

        self.__zfs_ebuild = 'sys-fs/zfs-kmod'
        if self.__use_zfs_version == 'release':
            for ebuilds in os.listdir(f'{self.__port}/{self.__zfs_ebuild}'):
                if 'ebuild' in ebuilds and '9999' not in ebuilds:
                    self.__zver = sorted(os.listdir(
                            f'{self.__port}/{self.__zfs_ebuild}'))[-1].rpartition('.')[0].rpartition('-')[-1]

            self.__kmod = "zfs"  # build path
        else:
            # git
            self.__zver = '9999'
            self.__kmod = 'zfs-kmod'  # build path

        self.__zfs_ebuild_full = f'{self.__port}/{self.__zfs_ebuild}/zfs-kmod-{self.__zver}.ebuild'
        if not os.path.isfile(f'{self.__zfs_ebuild_full}'):
            utils.die(message=f'ERROR: missing \'{self.__zfs_ebuild_full}\'')

        self.__kmod_src = f'{self.__storage}/src/{self.__kver}/{self.__zver}'
        if not os.path.isdir(self.__kmod_src) and self.__run_zfs_build:
            # need to build if configured src do not exists
            self.__run_kmod_build = True

    def run_zfs_build(self):
        zver_path = self.__zver

        if 'rc' in self.__zver:
            # rc ebuilds
            self.__zver = self.__zver.rpartition('_')[0]
        if '-r' in self.__zver:
            # rev bump ebuilds
            self.__zver = self.__zver.rpartition('-')[0]

        archive = f'zfs-{self.__zver}.tar.zst'

        if self.__run_kmod_build:
            self.cdkdir()
            self.msc()

            if not self.__use_modules:
                shutil.move(f'{self.__kdir}/.config', f'{self.__tmpdir}/.config')
                shutil.copyfile(self.__switch_kconf, f'{self.__kdir}/.config')

            # FIXME does not work if CC=clang
            # utils.run_cmd(f'{self.__kmake} prepare')
            utils.run_cmd('make CC=gcc LD=ld.bfd prepare')

            if os.path.isdir(self.__kmod_src):
                shutil.rmtree(self.__kmod_src)
            pathlib.Path(self.__kmod_src).mkdir(parents=True, exist_ok=True)

            portage_env = f'export PORTAGE_TMPDIR="{self.__tmpdir}"\n'
            if self.__use_distdir:
                portage_env += f'export DISTDIR="{self.__storage}/distfiles"\n'

            # this is just simpler
            script = f'{self.__tmpdir}/tmp.sh'
            text = '#!/usr/bin/env sh\n' \
                   f'die(){{ /bin/echo -e $*;kill {os.getpid()}; }}\n' \
                   f'{portage_env}\n' \
                   f'EXTRA_ECONF="--with-linux={self.__kdir} --enable-linux-builtin" ebuild ' \
                   f'{self.__zfs_ebuild_full} configure || die "build failed"\n' \
                   f'cd {self.__tmpdir}/portage/{self.__zfs_ebuild}-{zver_path}/work/{self.__kmod}-{self.__zver}\n' \
                   f'./copy-builtin {self.__kdir} || die "copy-builtin failed"\n' \
                   'cd ..\n' \
                   f'tar -cf - {self.__kmod}-{self.__zver} -P | zstd -T0 -4 >| {archive}\n' \
                   f'mv {archive} {self.__kmod_src}'

            utils.write_script(script, text)
            utils.run_cmd(script)

            if self.__cc_use_clang:
                utils.run_cmd('kernel-clean-src -c')

            if not self.__use_modules:
                os.remove(f'{self.__kdir}/.config')
                shutil.copyfile(f'{self.__kdir}/.config', self.__switch_kconf)

            if self.__clean_kernel_src:
                utils.run_cmd('sh -c "kernel-clean-src -c"')

        else:
            if not os.path.isfile(f'{self.__kmod_src}/{archive}'):
                utils.die(message=f'Archive missing: {self.__kmod_src}/{archive}')

            # this is just simpler
            script = f'{self.__tmpdir}/tmp.sh'
            text = '#!/usr/bin/env sh\n' \
                   f'die(){{ /bin/echo -e $*;kill {os.getpid()}; }}\n' \
                   f'cd {self.__kmod_src} || die "cd failed"\n' \
                   f'tar -I zstd -xf {archive} -C {self.__tmpdir} || die "extraction failed"\n' \
                   f'cd {self.__tmpdir}/{self.__kmod}-{self.__zver}\n' \
                   f'./copy-builtin {self.__kdir} || die "copy-builtin failed"'

            utils.write_script(script, text)
            utils.run_cmd(script)

    def run_kernel_build(self):
        self.cdkdir()
        self.msc()
        utils.run_cmd(f'sh -c "{self.__kmake}"')

        if self.__run_kernel_install:
            if self.__use_modules:
                utils.run_cmd(f'sh -c "{self.__kmake}" modules_install')
            utils.run_cmd(f'sh -c "{self.__kmake}" install')

        if self.__run_kernel_post:
            if self.__run_emerge:
                if self.__run_kmod_build:
                    if self.__use_zfs_version == 'release':
                        utils.run_cmd('emerge --ignore-default-opts --oneshot --quiet --update sys-fs/zfs')
                    else:
                        # will always rebuild zfs when using git
                        utils.run_cmd('emerge --ignore-default-opts --oneshot --quiet sys-fs/zfs')
                if self.__use_modules:
                    utils.run_cmd('emerge --ignore-default-opts --oneshot --jobs @module-rebuild')
            utils.run_cmd(f'kernel-initramfs-dracut -k {self.__kver_full}')
            utils.run_cmd('kernel-grub')
            if self.__clean_kernel_src:
                utils.run_cmd('kernel-clean-src -c')

    def build(self):
        self.set_compiler()
        self.modules_check()

        if self.__run_zfs_checks:
            self.run_zfs_checks()
        if self.__run_intro:
            self.intro()
        if self.__run_kernel_bump or self.__force_bump_check:
            self.kernel_bump()
        if self.__run_zfs_build:
            self.run_zfs_build()
        if self.__run_kernel_build:
            self.run_kernel_build()

    def run(self, args):
        # General
        if args.force_no_bump:
            self.__force_bump_check = False
        if args.force_bump:
            self.__force_bump_check = True
        if args.edit:
            utils.edit_conf(self.__settings)
        if args.reset_config:
            os.remove(self.__settings)
        if args.rm_built_src:
            shutil.rmtree(f'{self.__storage}/distfiles')
            shutil.rmtree(f'{self.__storage}/src')
            os.mkdir(f'{self.__storage}/distfiles')
            os.mkdir(f'{self.__storage}/src')
        if args.no_intro:
            self.__run_intro = False
        if args.verbose:
            self.__intro_extra = True
        # ZFS
        if args.force_rebuild_kmod:
            self.__run_kmod_build = True
        if args.local_distdir:
            self.__use_distdir = True
        if args.use_git:
            self.__use_zfs_version = 'git'
        if args.use_release:
            self.__use_zfs_version = 'release'
        if args.use_local_ebuild:
            self.__use_local_zfs_ebuild = True
        # Kernel
        if args.compiler:
            self.__cc_use_clang = True
        if args.no_clean:
            self.__clean_kernel_src = False
        if args.emerge:
            self.__run_emerge = True
        if args.no_install:
            self.__run_kernel_post = False
            self.__run_kernel_install = False
        if args.modules:
            self.__use_modules = True
        if args.no_post:
            self.__run_kernel_post = True
        if args.fancy_make:
            self.__run_zfs_checks = False
            self.__run_zfs_build = False
        if args.zfs_install:
            self.__run_zfs_build = True
            self.__run_kernel_build = False

        self.build()


def main():
    parser = argparse.ArgumentParser()
    general = parser.add_argument_group('GENERAL')
    general.add_argument('-b', '--force-no-bump',
                         action='store_true',
                         help='force disable kernel bump check')
    general.add_argument('-B', '--force-bump',
                         action='store_true',
                         help='force enable kernel bump check')
    general.add_argument('-E', '--edit',
                         action='store_true',
                         help='Edit config file')
    general.add_argument('-I', '--no-intro',
                         action='store_true',
                         help='disable intro')
    general.add_argument('-R', '--reset-config',
                         action='store_true',
                         help='reset config file and exit')
    general.add_argument('--rm-built-src',
                         action='store_true',
                         help='Remove script generated \'distfiles\' and \'src\' dirs')
    general.add_argument('-v', '--verbose',
                         action='store_true',
                         help='set verbose on')
    zfs = parser.add_argument_group('ZFS')
    zfs.add_argument('-c', '--force-rebuild-kmod',
                     action='store_true',
                     help='build kmod even if preconfigured sources exist')
    zfs.add_argument('-d', '--local-distdir',
                     action='store_true',
                     help='use $XDG_DATA_DIR/kenrel/distfiles as $DISTDIR, does not work with FEATURES=userfetch')
    zfs.add_argument('-g', '--use-git',
                     action='store_true',
                     help='use git ebuild')
    zfs.add_argument('-r', '--use-release',
                     action='store_true',
                     help='use release ebuild')
    zfs.add_argument('-l', '--use-local-ebuild',
                     action='store_true',
                     help='use local repo in $PORTDIR_OVERLAY')
    ker = parser.add_argument_group('KERNEL')
    ker.add_argument('-G', '--compiler',
                     action='store_true',
                     help='build kernel using clang')
    ker.add_argument('-C', '--no-clean',
                     action='store_true',
                     help='disable cleaning kernel source dir')
    ker.add_argument('-e', '--emerge',
                     action='store_true',
                     help='enable running emerge in post')
    ker.add_argument('-i', '--no-install',
                     action='store_true',
                     help='build kernel but do not install or run post, implies -p')
    ker.add_argument('-m', '--modules',
                     action='store_true',
                     help='force enable module build')
    ker.add_argument('-p', '--no-post',
                     action='store_true',
                     help='disable post, emerge, initramfs, and grub configure')
    ker.add_argument('-x', '--fancy-make',
                     action='store_true',
                     help='disable zfs build, becomes fancy \'make;make install\'')
    ker.add_argument('-z', '--zfs-install',
                     action='store_true',
                     help='only run zfs build, will install zfs into kenrel tree')

    args = parser.parse_args()

    utils.is_root()

    run = Build()
    run.run(args)


if __name__ == '__main__':
    main()
