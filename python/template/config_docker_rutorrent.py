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

# https://github.com/crazy-max/docker-rtorrent-rutorrent

## PORTS ##
# 6881 (or RT_DHT_PORT): DHT UDP port (dht.port.set)
# 8000 (or XMLRPC_PORT): XMLRPC port through nginx over SCGI socket
# 8080 (or RUTORRENT_PORT): ruTorrent HTTP port
# 9000 (or WEBDAV_PORT): WebDAV port on completed downloads
# 50000 (or RT_INC_PORT): Incoming connections (network.port_range.set)
# Port p+1 for XMLRPC_PORT, RUTORRENT_PORT and WEBDAV_PORT are reserved for healthcheck.

class _DockerTorrentConfig:
    def __init__(self):
        # copy to python/private/config_lxd.py to use

        self.CONFIG_VERSION = 1

        self.CONFIG = {
            'ANIME':
                {
                    'ENABLED': True,
                    'AUTOSTART': True,
                    'NAME': 'anime',
                    'PORT_6881' : '6881',
                    'PORT_8000' : '8000', # port p+1 will be reserved
                    'PORT_8080' : '8080', # port p+1 will be reserved
                    'PORT_9000' : '9000', # port p+1 will be reserved
                    'PORT_50000' : '50000',
                    'PATH_DATA' : '/mnt/cache/anime',
                    'PATH_DOWNLOADS' : '/mnt/anime/downloads',
                },
            'ANIME2':
                {
                    'ENABLED': True,
                    'AUTOSTART': True,
                    'NAME': 'anime',
                    'PORT_6882' : '6882',
                    'PORT_8002' : '8002', # port p+1 will be reserved
                    'PORT_8082' : '8082', # port p+1 will be reserved
                    'PORT_9002' : '9002', # port p+1 will be reserved
                    'PORT_50001' : '50002',
                    'PATH_DATA' : '/mnt/cache/anime2',
                    'PATH_DOWNLOADS' : '/mnt/anime/downloads2',
                },
        }


DockerTorrentConfig = _DockerTorrentConfig()
