# -*- coding: utf-8 -*-
# 2.7.0
# 2021-01-12

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
import sys
from pathlib import Path

from loguru import logger

from python.utils.execute import Execute
from python.utils.lxd import Lxd

try:
    from python.private.config_lxd import LxdConfig
except ImportError:
    print('Missing config file, see python/template/config_lxd.py')
    raise SystemExit(1)


# TODO
#   Execute() will block until cmd returns,
#       therfore forking to speed up commands does not work
#   possible config changes
#       more limits
#       drop self.__container_type
#       drop self.__container_distro


class Container:
    def __init__(self):
        super().__init__()

        self.__CONFIG_VERSION = 5

        if self.__CONFIG_VERSION != LxdConfig.CONFIG_VERSION:
            logger.critical('config versions do not match, update config to new format')
            raise SystemExit(1)

        self.__action = None

        self.__only_container = None
        self.__catch_single = False

        self.__create_missing_dirs = False

        self.__service = None

        self.__print_verbose = False

        self.__ip4_brd = '192.168.0.255'
        self.__ip4_gateway = '192.168.0.1'
        self.__ip4_netmask = '255.255.255.0'

        self.__clean_lockfiles = False
        self.__clean_torrents = False

        # container name and config/data paths
        self.__container_fullname = None
        self.__container_template = None

        # paths not in container
        self.__container_path_storage = Path() / '/mnt/torrents'
        self.__container_path_config = None
        self.__container_path_session = None
        self.__container_path_watch = None
        self.__container_path_save = None
        self.__container_path_rushare = None

        # paths in container
        self.__container_inside_path_rushare = None
        self.__container_inside_path_home = None
        self.__container_inside_path_watch = None
        self.__container_inside_path_data = None
        self.__container_inside_path_session = None

        # filled by config file
        self.__container_type = None
        self.__container_distro = None
        self.__container_user = None
        self.__container_autostart = False
        self.__container_htpasswd = False
        self.__container_ipv4 = None
        self.__container_limit_cpu = None
        self.__container_limit_cpu_allowance = None
        self.__container_limit_mem = None
        self.__container_name = None
        self.__container_save_override = None

    def print_config(self, verbose: bool = False):
        print(f'Container Name      : {self.__container_fullname}\n'
              f'Base Name           : {self.__container_name}\n'
              f'Template            : {self.__container_type}\n'
              f'Distro              : {self.__container_distro}\n'
              f'IPV4                : {self.__container_ipv4}\n'
              f'Running             : {Lxd.get_state(container=self.__container_fullname)}\n'
              f'Autostart           : {self.__container_autostart}\n'
              f'Container User      : {self.__container_user}')
        if verbose:
            print(f'using htpasswd      : {self.__container_htpasswd}\n'
                  f'Limit CPU           : {self.__container_limit_cpu}\n'
                  f'Limit CPU ALLOW     : {self.__container_limit_cpu_allowance}\n'
                  f'Limit MEM           : {self.__container_limit_mem}\n'
                  'IN CONTAINER PATHS\n'
                  f'home path           : {self.__container_inside_path_home}\n'
                  f'session path        : {self.__container_inside_path_session}\n'
                  f'watch path          : {self.__container_inside_path_watch}\n'
                  f'data path           : {self.__container_inside_path_data}\n'
                  f'rushare path        : {self.__container_inside_path_rushare}\n'
                  'HOST PATHS\n'
                  f'config path         : {self.__container_path_config}\n'
                  f'session path        : {self.__container_path_session}\n'
                  f'watch path          : {self.__container_path_watch}\n'
                  f'rushare path        : {self.__container_path_rushare}\n'
                  f'save path           : {self.__container_path_save}\n'
                  f'save override path  : {self.__container_save_override}')

        print('\n')

    def set_dirs(self):
        # paths from host
        self.__container_path_config = Path() / self.__container_path_storage / '.config' / self.__container_name
        self.__container_path_session = Path() / self.__container_path_config / 'session'
        self.__container_path_watch = Path() / self.__container_path_config / 'watch'
        self.__container_path_save = Path() / self.__container_path_storage / self.__container_name
        self.__container_path_rushare = Path() / self.__container_path_config / 'rutorrent/share'
        if self.__container_save_override is not None:
            self.__container_path_save = Path() / self.__container_save_override

        # paths in container
        self.__container_inside_path_rushare = Path() / '/var/www/localhost/htdocs/rutorrent/share'
        self.__container_inside_path_home = Path() / '/home' / self.__container_user
        self.__container_inside_path_data = Path() / self.__container_inside_path_home / 'rtorrent/data'
        self.__container_inside_path_watch = Path() / self.__container_inside_path_home / 'rtorrent/watch'
        self.__container_inside_path_session = Path() / self.__container_inside_path_home / 'rtorrent/session'

        if self.__create_missing_dirs:
            # create config dirs if they are missing
            if not Path.exists(self.__container_path_config):
                logger.info(f'Creating missing dir: \'{self.__container_path_config}\'')
                self.__container_path_config.mkdir(parents=True, exist_ok=True)
            if not Path.exists(self.__container_path_session):
                logger.info(f'Creating missing dir: \'{self.__container_path_session}\'')
                self.__container_path_session.mkdir(parents=True, exist_ok=True)
            if not Path.exists(self.__container_path_watch):
                logger.info(f'Creating missing dir: \'{self.__container_path_watch}\'')
                self.__container_path_watch.mkdir(parents=True, exist_ok=True)
            if not Path.exists(self.__container_path_save):
                logger.info(f'Creating missing dir: \'{self.__container_path_save}\'')
                self.__container_path_save.mkdir(parents=True, exist_ok=True)
            if not Path.exists(self.__container_path_rushare):
                logger.info(f'Creating missing dir: \'{self.__container_path_rushare}\'')
                self.__container_path_rushare.mkdir(parents=True, exist_ok=True)
            if not Path.exists(self.__container_path_save):
                logger.info(f'Creating missing dir: \'{self.__container_path_save}\'')
                self.__container_path_save.mkdir(parents=True, exist_ok=True)

    def attach_dirs(self):
        Execute(f'lxc config device add {self.__container_fullname} storage disk '
                f'source="{self.__container_path_save}" path="{self.__container_inside_path_data}"',
                to_stdout=True)
        Execute(f'lxc config device add {self.__container_fullname} session disk '
                f'source="{self.__container_path_session}" path="{self.__container_inside_path_session}"',
                to_stdout=True)
        Execute(f'lxc config device add {self.__container_fullname} watch disk '
                f'source="{self.__container_path_watch}" path="{self.__container_inside_path_watch}"',
                to_stdout=True)
        Execute(f'lxc config device add {self.__container_fullname} ru disk '
                f'source="{self.__container_path_rushare}" path={self.__container_inside_path_rushare}',
                to_stdout=True)

    def stop(self):
        if not Lxd.get_state(container=self.__container_fullname):
            return

        logger.info(f'Stopping container: {self.__container_fullname}')
        Execute(f'lxc stop {self.__container_fullname}', to_stdout=True)

    def start(self):
        if Lxd.get_state(container=self.__container_fullname):
            logger.info(f'Already started: {self.__container_fullname}')
            return

        if not self.__container_autostart:
            return

        # remove rtorrent lockfiles since they can persist
        # and do not always work even between restart of the same
        # container, overall they are just annoying
        # Execute(f'{CheckEnv.get_script_name()} -c -O {self.__container_fullname}')
        self.rtorrent_clean_torrent()

        logger.info(f'Starting container: {self.__container_fullname}')
        Execute(f'lxc start {self.__container_fullname}', to_stdout=True)

    def delete(self):
        if Lxd.get_state(container=self.__container_fullname):
            logger.warning(f'Must stop before deleting {self.__container_fullname}')
            return

        logger.info(f'Deleting container: {self.__container_fullname}')
        Execute(f'lxc delete {self.__container_fullname}', to_stdout=True)

    def restart(self):
        if not Lxd.get_state(container=self.__container_fullname):
            return

        logger.info(f'Restarting container: {self.__container_fullname}')
        Execute(f'lxc restart {self.__container_fullname}', to_stdout=True)

    def forcestop(self):
        if not Lxd.get_state(container=self.__container_fullname):
            return

        logger.info(f'Force Stopping container: {self.__container_fullname}')
        Execute(f'lxc stop --force {self.__container_fullname}', to_stdout=True)

    def restart_service(self):
        if not Lxd.get_state(container=self.__container_fullname):
            return

        logger.info(f'Restarting \'{self.__service}\' on \'{self.__container_fullname}\'')
        Execute(f'lxc exec {self.__container_fullname} rc-service {self.__service} restart', to_stdout=True)

    def rtorrent_clean_lock(self):
        if Lxd.get_state(container=self.__container_fullname):
            logger.warning(f'Not cleaning lock on running {self.__container_fullname}')
            return

        lockfile = Path() / self.__container_path_session / 'rtorrent.lock'
        logger.debug(f'Cleaning lock file {lockfile}')
        if Path.exists(lockfile):
            logger.info(f'Removed lockfile {lockfile}')
            lockfile.unlink()

    def rtorrent_clean_torrent(self):
        if self.__container_htpasswd:
            torrent_files_path = Path() / self.__container_path_rushare / 'users' / self.__container_user / 'torrents'
        else:
            torrent_files_path = Path() / self.__container_path_rushare / 'torrents'

        logger.debug(f'Cleaning *.torrent files in {torrent_files_path}')

        for f in torrent_files_path.iterdir():
            if Path.is_file(f) and str(f).endswith('.torrent'):
                f.unlink()

    def update(self):
        if Lxd.get_state(container=self.__container_fullname):
            logger.error(f'Not updating running container: {self.__container_fullname}')
            return

        if Lxd.get_state(container=self.__container_template):
            # could stop template here but it could be doing something, ie updating
            logger.error(f'Not running update when template is running: {self.__container_template}')
            return

        logger.info(f'Running update for: {self.__container_fullname}')

        check_exists = Execute(f'lxc list | grep {self.__container_fullname}',
                               sh_wrap=True, to_stdout=True).get_out()
        if check_exists:
            logger.info(f'Deleting: {self.__container_fullname}')
            Execute(f'lxc delete {self.__container_fullname}', to_stdout=True)

        logger.info(f'Copying: {self.__container_template} to {self.__container_fullname}')
        Execute(f'lxc copy {self.__container_template} {self.__container_fullname}')

        # removes unneeded access to filesystem on gentoo containers
        logger.info(f'Removing unneeded access to filesystem')
        Execute(f'lxc config device remove {self.__container_fullname} distfiles', to_stdout=True)
        Execute(f'lxc config device remove {self.__container_fullname} packages', to_stdout=True)
        Execute(f'lxc config device remove {self.__container_fullname} repos', to_stdout=True)

        # set cpu/mem limits
        if self.__container_limit_cpu != '0':
            logger.info(f'Setting CPU Limit to {self.__container_limit_cpu}')
            Execute(f'lxc config set {self.__container_fullname} '
                    f'limits.cpu {self.__container_limit_cpu}', to_stdout=True)
        if self.__container_limit_cpu_allowance != '0':
            logger.info(f'Setting CPU Allowance Limit to {self.__container_limit_cpu_allowance}')
            Execute(f'lxc config set {self.__container_fullname} '
                    f'limits.cpu.allowance {self.__container_limit_cpu_allowance}', to_stdout=True)
        if self.__container_limit_mem != '0':
            logger.info(f'Setting MEM Limit to {self.__container_limit_mem}')
            Execute(f'lxc config set {self.__container_fullname} '
                    f'limits.memory {self.__container_limit_mem}', to_stdout=True)

        # remove rtorrent lockfiles since they can persist
        # and do not work between container upgrades
        self.rtorrent_clean_lock()

        # set container ipv4
        logger.info(f'Seting StaticIP to: {self.__container_ipv4}')
        net_tmp = Path() / '/tmp/lxd-net-tmp'  # TODO - use tempfile and not hardcoded path
        net_real = Path() / self.__container_fullname / 'etc/conf.d/net'
        net_config = f'rc_keyword="-stop"\n' \
                     f'config_eth0="{self.__container_ipv4} netmask {self.__ip4_netmask} brd {self.__ip4_brd}"\n' \
                     f'routes_eth0="default via {self.__ip4_gateway}"\n'

        net_tmp.write_text(net_config)

        Execute(f'lxc file push {net_tmp} {net_real}')
        net_tmp.unlink()

        # attach storage dirs to container
        self.attach_dirs()

    def main(self):
        container_config = LxdConfig.CONFIG

        for idx, item in enumerate(container_config):
            if not container_config[item]['ENABLED']:
                continue

            self.__container_type = container_config[item]['TYPE']
            self.__container_distro = container_config[item]['DISTRO']
            self.__container_user = container_config[item]['USER']
            self.__container_autostart = container_config[item]['AUTOSTART']
            self.__container_htpasswd = container_config[item]['HTPASSWD']
            self.__container_ipv4 = container_config[item]['IPV4']
            self.__container_limit_cpu = container_config[item]['LIMIT_CPU']
            self.__container_limit_cpu_allowance = container_config[item]['LIMIT_CPU_ALLOWANCE']
            self.__container_limit_mem = container_config[item]['LIMIT_MEM']
            self.__container_name = container_config[item]['NAME']
            self.__container_save_override = container_config[item]['SAVE_OVERRIDE']

            # create actual container name
            self.__container_fullname = f'{self.__container_type}-{self.__container_name}'
            self.__container_template = f'base-{self.__container_distro}-{self.__container_type}'

            if self.__catch_single:
                if self.__container_fullname != self.__only_container:
                    continue

            self.set_dirs()

            # wish python had a switch
            if self.__action == 'start':
                self.start()
            elif self.__action == 'stop':
                self.stop()
            elif self.__action == 'forcestop':
                self.forcestop()
            elif self.__action == 'restart':
                self.restart()
            elif self.__action == 'delete':
                self.delete()
            elif self.__action == 'update':
                self.update()
            elif self.__action == 'service':
                self.restart_service()
            elif self.__clean_lockfiles:
                self.rtorrent_clean_lock()
            elif self.__clean_torrents:
                self.rtorrent_clean_torrent()
            elif self.__action == 'print':
                self.print_config(self.__print_verbose)

    def run(self, args):
        # container
        if args.only:
            self.__only_container = args.only
            self.__catch_single = True
        # container services
        if args.service:
            self.__action = 'service'
            self.__service = args.service
        # container general
        if args.delete:
            self.__action = 'delete'
        if args.restart:
            self.__action = 'restart'
        if args.start:
            self.__action = 'start'
        if args.update:
            self.__action = 'update'
        if args.stop:
            self.__action = 'stop'
        if args.force_stop:
            self.__action = 'forcestop'
        if args.create_dirs:
            self.__create_missing_dirs = True
        # specific
        if args.rutorrent_lockfile:
            self.__clean_lockfiles = True
        if args.rutorrent_torrents:
            self.__clean_torrents = True
        # other
        if args.print:
            self.__action = 'print'
        if args.print_verbose:
            self.__action = 'print'
            self.__print_verbose = True

        self.main()


def main():
    parser = argparse.ArgumentParser()
    container = parser.add_argument_group('container')
    container.add_argument('-O', '--only',
                           metavar='CONTAINER',
                           help='Only operate in the supplied container, requires full container name')
    service = parser.add_argument_group('container services')
    service.add_argument('-S', '--service',
                         metavar='SERVICE',
                         help='restart service passed as arg')
    service.add_argument('--create-dirs',
                         action='store_true',
                         help='Create container storage dirs if the do not exist')
    # required = parser.add_argument_group('container general').add_mutually_exclusive_group(required=True)
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
    required.add_argument('-z', '--stop',
                          action='store_true',
                          help='Stop containers')
    required.add_argument('-Z', '--force-stop',
                          action='store_true',
                          help='Force stop containers')
    clean = parser.add_argument_group('rutorrent only').add_mutually_exclusive_group()
    clean.add_argument('-c', '--rutorrent-lockfile',
                       action='store_true',
                       help='rtorrent lockfile cleanup')
    clean.add_argument('-C', '--rutorrent-torrents',
                       action='store_true',
                       help='rutorrent cleanup only, remove *.torrent files in $config/rutorrent/share/torrents/')
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

    run = Container()
    run.run(args)
