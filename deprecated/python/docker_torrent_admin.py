#!/usr/bin/env python3

# Copyright (C) 2018-2023 Brandon Zorn <brandonzorn@cock.li>
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
# 2023-08-17


import argparse
import sys
from pathlib import Path

from loguru import logger

from utils.execute import Execute
# from utils.script import ExecuteBashScript

try:
    from private.config_docker_rutorrent import DockerTorrentConfig
except ImportError:
    print('Missing config file, see python/template/config_docker_rutorrent.py')
    raise SystemExit(1)

class Container:
    def __init__(self, args: argparse = None):
        super().__init__()

        self.__CONFIG_VERSION = 1

        if self.__CONFIG_VERSION != DockerTorrentConfig.CONFIG_VERSION:
            logger.critical('config versions do not match, update config to new format')
            raise SystemExit(1)

        self.__action = None

        self.__only_container = None
        self.__catch_single = False

        self.__print_verbose = False

        self.__container_name: str = None

        # filled by config file
        self.__container_autostart: bool = False
        self.__container_base_name: str = None
        self.__container_port_6881: int = None
        self.__container_port_8000: int = None
        self.__container_port_8080: int = None
        self.__container_port_9000: int = None
        self.__container_port_50000: int = None
        self.__container_path_data: Path = None
        self.__container_path_downloads: Path = None

        self.parse_args(args=args)

        self.main()

    def print_config(self, verbose: bool = False):
        print(f'Container Name      : {self.__container_name}\n'
              f'Address             : 127.0.0.1:{self.__container_port_8080}')
        if verbose:
            print(f'Autostart           : {self.__container_autostart}\n'
                  f'port 6881/udp       : {self.__container_port_6881}\n'
                  f'port 8000           : {self.__container_port_8000}\n'
                  f'port 8080           : {self.__container_port_8080}\n'
                  f'port 9000           : {self.__container_port_9000}\n'
                  f'port 50000          : {self.__container_port_50000}\n'
                  f'path data           : {self.__container_path_data}\n'
                  f'path downloads      : {self.__container_path_downloads}')
        print()

    def stop(self):
        logger.info(f'Stopping container: {self.__container_name}')
        Execute(f'docker stop {self.__container_name}', to_stdout=True, blocking=False)

    def start(self):
        logger.info(f'Starting container: {self.__container_name}')
        Execute(f'docker start {self.__container_name}', to_stdout=True)

    def delete(self):
        self.stop()
        logger.info(f'Deleting container: {self.__container_name}')
        Execute(f'docker rm {self.__container_name}', to_stdout=True)

    def restart(self):
        logger.info(f'Restarting container: {self.__container_name}')
        Execute(f'docker restart {self.__container_name}', to_stdout=True)

    def update(self):
        logger.info(f'Running update for: {self.__container_name}')

        self.stop()

        update_sh = f"""
            docker run -d --name {self.__container_name} \
            --ulimit nproc=65535 \
            --ulimit nofile=32000:40000 \
            -p {self.__container_port_6881}:6881/udp \
            -p {self.__container_port_8000}:8000 \
            -p {self.__container_port_8080}:8080 \
            -p {self.__container_port_9000}:9000 \
            -p {self.__container_port_50000}:50000 \
            -e MAX_FILE_UPLOADS=200 \
            -v {self.__container_path_data}:/data \
            -v {self.__container_path_downloads}:/downloads \
            ghcr.io/crazy-max/rtorrent-rutorrent
        """

        Execute(update_sh, to_stdout=True)

    def update_image(self):
        Execute("docker pull ghcr.io/crazy-max/rtorrent-rutorrent:latest")


    def main(self):
        container_config = DockerTorrentConfig.CONFIG

        for item in container_config:
            if not container_config[item]['ENABLED']:
                continue

            self.__container_autostart = container_config[item]['AUTOSTART']
            self.__container_base_name = container_config[item]['NAME']
            self.__container_port_6881 = container_config[item]['PORT_6881']
            self.__container_port_8000 = container_config[item]['PORT_8000']
            self.__container_port_8080 = container_config[item]['PORT_8080']
            self.__container_port_9000 = container_config[item]['PORT_9000']
            self.__container_port_50000 = container_config[item]['PORT_50000']
            self.__container_path_data = container_config[item]['PATH_DATA']
            self.__container_path_downloads = container_config[item]['PATH_DOWNLOADS']

            if self.__catch_single:
                if self.__container_name != self.__only_container:
                    continue

            self.__container_name = f'rutorrent_{self.__container_base_name}'

            # wish python had a switch
            if self.__action == 'start':
                self.start()
            elif self.__action == 'stop':
                self.stop()
            elif self.__action == 'restart':
                self.restart()
            elif self.__action == 'delete':
                self.delete()
            elif self.__action == 'update':
                self.update()
            elif self.__action == 'update-image':
                self.update_image()
            elif self.__action == 'print':
                self.print_config(self.__print_verbose)

    def parse_args(self, args):
        # container
        if args.only:
            self.__only_container = args.only
            self.__catch_single = True
        # container general
        if args.delete:
            self.__action = 'delete'
        if args.restart:
            self.__action = 'restart'
        if args.start:
            self.__action = 'start'
        if args.update:
            self.__action = 'update'
        if args.update_image:
            self.__action = 'update-image'
        if args.stop:
            self.__action = 'stop'
        # other
        if args.print:
            self.__action = 'print'
        if args.print_verbose:
            self.__action = 'print'
            self.__print_verbose = True


def main():
    parser = argparse.ArgumentParser()
    container = parser.add_argument_group('container')
    container.add_argument('-O', '--only',
                           metavar='CONTAINER',
                           help='Only operate in the supplied container, requires full container name')
    required = parser.add_argument_group('container general').add_mutually_exclusive_group()
    required.add_argument('-d', '--delete',
                          action='store_true',
                          help='Delete containers')
    required.add_argument('-r', '--restart',
                          action='store_true',
                          help='Restart containers')
    required.add_argument('-s', '--start',
                          action='store_true',
                          help='Start containers')
    required.add_argument('-u', '--update',
                          action='store_true',
                          help='Update containers')
    required.add_argument('-U', '--update-image',
                          action='store_true',
                          help='Update base image')
    required.add_argument('-z', '--stop',
                          action='store_true',
                          help='Stop containers')
    dbg_print = parser.add_argument_group('print container vars').add_mutually_exclusive_group()
    dbg_print.add_argument('-p', '--print',
                           action='store_true',
                           help='Print all container vars')
    dbg_print.add_argument('-P', '--print-verbose',
                           action='store_true',
                           help='Print limited container vars')
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

    Container(args=args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
