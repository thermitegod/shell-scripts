# -*- coding: utf-8 -*-

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
# 1.0.0
# 2020-11-02


class _LxdConfig:
    def __init__(self):
        """
        Current format

        'ENABLED', bool, enable or disable container.
        'TYPE', str, which torrent client to use, only rtorrent.
        'DISTRO': str, which distro to use, only gentoo
        'USER': str, user to use in container
        'AUTOSTART': bool, start container with -s
        'HTPASSWD': bool, use htpasswd for rutorrent web ui
        'IPV4': str, a local ipv4 address
        'LIMIT_CPU': str, cpu core limit
        'LIMIT_CPU_ALLOWANCE': str, cpu allowance
        'LIMIT_MEM': str, mem limit
        'NAME': str, container name
        'SAVE_OVERRIDE': str, override default save path, absolute path
        """

        # copy to python/private/config_lxd.py to use

        self.CONFIG_VERSION = 5

        self.CONFIG = {
            'ANIME':
                {
                    'ENABLED': True,
                    'TYPE': 'rutorrent',
                    'DISTRO': 'gentoo',
                    'USER': 'brandon',
                    'AUTOSTART': True,
                    'HTPASSWD': True,
                    'IPV4': '192.168.0.161',
                    'LIMIT_CPU': '4',
                    'LIMIT_CPU_ALLOWANCE': '5%',
                    'LIMIT_MEM': '4096MB',
                    'NAME': 'anime',
                    'SAVE_OVERRIDE': '/mnt/anime/anime-working',
                },
            'ANIME2':
                {
                    'ENABLED': True,
                    'TYPE': 'rutorrent',
                    'DISTRO': 'gentoo',
                    'USER': 'brandon',
                    'AUTOSTART': True,
                    'HTPASSWD': True,
                    'IPV4': '192.168.0.162',
                    'LIMIT_CPU': '4',
                    'LIMIT_CPU_ALLOWANCE': '1%',
                    'LIMIT_MEM': '4096MB',
                    'NAME': 'anime2',
                    'SAVE_OVERRIDE': None,
                },
        }


LxdConfig = _LxdConfig()
