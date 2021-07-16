# -*- coding: utf-8 -*-
# 1.0.0
# 2021-07-16

# Copyright (C) 2021 Brandon Zorn <brandonzorn@cock.li>
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
import shutil
import sys
from pathlib import Path

from loguru import logger

from python.utils.execute import Execute


class Vscode:
    def __init__(self):
        config_base = Path() / os.environ['XDG_CONFIG_HOME'] / 'vscode'

        config = Path() / config_base / 'config'
        if not config.is_dir():
            config.mkdir(parents=True, exist_ok=True)

        extensions = Path() / config_base / 'extensions'
        if not extensions.is_dir():
            extensions.mkdir(parents=True, exist_ok=True)

        vscode_cache_base = Path() / os.environ['XDG_CACHE_HOME'] / 'vscode_cache'
        if not vscode_cache_base.is_dir():
            vscode_cache_base.mkdir(parents=True, exist_ok=True)

        fake_home = config_base / 'fake_home'

        # remove extension dist files
        CachedExtensionVSIXs = Path() / config / 'CachedExtensionVSIXs'
        if CachedExtensionVSIXs.is_dir():
            for f in CachedExtensionVSIXs.iterdir():
                if f.is_file():
                    f.unlink()

        # dir 'Cache'
        vscode_cache = Path() / vscode_cache_base / 'Cache'
        vscode_cache_sym = Path() / config / 'Cache'
        self.symlink_cache(vscode_cache, vscode_cache_sym)

        # dir 'CachedData'
        vscode_cached_data = Path() / vscode_cache_base / 'CachedData'
        vscode_cached_data_sym = Path() / config / 'CachedData'
        self.symlink_cache(vscode_cached_data, vscode_cached_data_sym)

        # dir 'Code Cache'
        vscode_code_cache = Path() / vscode_cache_base / 'Code Cache'
        vscode_code_cache_sym = Path() / config / 'Code Cache'
        self.symlink_cache(vscode_code_cache, vscode_code_cache_sym)

        # dir 'GPUCache'
        vscode_gpu_cache = Path() / vscode_cache_base / 'GPUCache'
        vscode_gpu_cache_sym = Path() / config / 'GPUCache'
        self.symlink_cache(vscode_gpu_cache, vscode_gpu_cache_sym)

        # since using a fake $HOME, add symlinks for .themes and .icons
        home = Path.home()

        icons = home / '.icons'
        icons_sym = fake_home / '.icons'
        if not icons_sym.is_symlink():
            os.symlink(icons, icons_sym)

        themes = home / '.themes'
        themes_sym = fake_home / '.themes'
        if not themes_sym.is_symlink():
            os.symlink(themes, themes_sym)

        # vscode uses ~/.vscode for extensions but can be chaned with cli flags.
        # ~/.vscode/argv.json location cannot be set and the retards at M$
        # dont care, have to use fake $HOME to change where this gets created

        Execute(f'HOME="{fake_home}" /opt/vscode/bin/code --user-data-dir {config} --extensions-dir {extensions}', sh_wrap=True)

        # vscode forks, dont remove cache dirs

        # remove temp cache dirs
        #if vscode_cache_base.is_dir():
        #    logger.info(f'Removing cache dir: {vscode_cache_base}')
        #    # shutil.rmtree(vscode_cache_base)

    def symlink_cache(self, src, dst):
        if not src.is_dir():
            src.mkdir(parents=True, exist_ok=True)

        if not dst.is_symlink():
            if dst.is_dir():
                shutil.rmtree(dst)

            os.symlink(src, dst)


def main():
    parser = argparse.ArgumentParser()
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

    Vscode()
