#!/usr/bin/env python3
# 1.9.2
# 2020-10-08

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

import argparse
import os
import sys
from pathlib import Path

from loguru import logger

from utils import editor
from utils import utils
from utils import lxd


# TODO
#   utils.run_cmd() will block until cmd returns,
#       therfore forking to speed up commands does not work
#   possible config version 4
#       more limits
#       drop self.__container_type
#       drop self.__container_distro


class Container:
    def __init__(self):
        self.__CONFIG_VERSION = '3'
        self.__config = Path() / os.environ["XDG_DATA_HOME"] / 'shell/lxd-admin'

        self.__action = None

        self.__only = None
        self.__catch_single = False

        self.__create_missing_dirs = False

        self.__print = False
        self.__print_verbose = False

        self.__service = None

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
        self.__container_autostart = None
        self.__container_htpasswd = None
        self.__container_ipv4 = None
        self.__container_limit_cpu = None
        self.__container_limit_cpu_allowance = None
        self.__container_limit_mem = None
        self.__container_name = None
        self.__container_save_override = None

    def print_config(self):
        print(f'Container Name      : {self.__container_fullname}\n'
              f'Base Name           : {self.__container_name}\n'
              f'Template            : {self.__container_type}\n'
              f'Distro              : {self.__container_distro}\n'
              f'IPV4                : {self.__container_ipv4}\n'
              f'Running             : {lxd.get_state(container=self.__container_fullname)}\n'
              f'Autostart           : {self.__container_autostart}\n'
              f'Container User      : {self.__container_user}')
        if self.__print_verbose:
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

    def config_help(self):
        print('==SUBJECT TO CHANGE==\n\n'
              f'Config version: {self.__CONFIG_VERSION}\n'
              f'Config file: \'{self.__config}\'\n\n'
              'All containers are declared using the following space delimited format\n'
              'Valid values are\n'
              '================\n'
              'container type: rutorrent, stop\n'
              'distro: gentoo\n'
              'user: user used in container\n'
              'autostart: 0, 1\n'
              'htpasswd: 0, 1\n'
              'ipv4: a local ipv4 address\n'
              'limit cpu: any int\n'
              'limit cpu allowance: any percent\n'
              'limit mem: any int with a unit\n'
              'container name: any string\n'
              'save location override, optional: a path\n\n'

              'Example\n'
              '================\n'
              f'version {self.__CONFIG_VERSION}\n'
              'rutorrent gentoo brandon 1 1 192.168.0.161 6 10% 8192MB anime /mnt/anime/anime-working\n'

              'Config file parsing\n'
              '================\n'
              'supports comments, no inline comments\n'
              'Script will stop if \'container type\' is set to \'stop\'')

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
        utils.run_cmd(f'lxc config device add {self.__container_fullname} storage disk '
                      f'source="{self.__container_path_save}" path="{self.__container_inside_path_data}"',
                      to_stdout=True)
        utils.run_cmd(f'lxc config device add {self.__container_fullname} session disk '
                      f'source="{self.__container_path_session}" path="{self.__container_inside_path_session}"',
                      to_stdout=True)
        utils.run_cmd(f'lxc config device add {self.__container_fullname} watch disk '
                      f'source="{self.__container_path_watch}" path="{self.__container_inside_path_watch}"',
                      to_stdout=True)
        utils.run_cmd(f'lxc config device add {self.__container_fullname} ru disk '
                      f'source="{self.__container_path_rushare}" path={self.__container_inside_path_rushare}',
                      to_stdout=True)

    def stop(self):
        if not lxd.get_state(container=self.__container_fullname):
            return

        logger.info(f'Stopping container: {self.__container_fullname}')
        utils.run_cmd(f'lxc stop {self.__container_fullname}', to_stdout=True)

    def start(self):
        if lxd.get_state(container=self.__container_fullname):
            return

        if self.__container_autostart != '1':
            return

        logger.info(f'Starting container: {self.__container_fullname}')
        utils.run_cmd(f'lxc start {self.__container_fullname}', to_stdout=True)

    def delete(self):
        if lxd.get_state(container=self.__container_fullname):
            logger.warning(f'Must stop before deleting {self.__container_fullname}')
            return

        logger.info(f'Deleting container: {self.__container_fullname}')
        utils.run_cmd(f'lxc delete {self.__container_fullname}', to_stdout=True)

    def restart(self):
        if not lxd.get_state(container=self.__container_fullname):
            return

        logger.info(f'Restarting container: {self.__container_fullname}')
        utils.run_cmd(f'lxc restart {self.__container_fullname}', to_stdout=True)

    def forcestop(self):
        if not lxd.get_state(container=self.__container_fullname):
            return

        logger.info(f'Force Stopping container: {self.__container_fullname}')
        utils.run_cmd(f'lxc stop --force {self.__container_fullname}', to_stdout=True)

    def restart_service(self):
        if not lxd.get_state(container=self.__container_fullname):
            return

        logger.info(f'Restarting \'{self.__service}\' on \'{self.__container_fullname}\'')
        utils.run_cmd(f'lxc exec {self.__container_fullname} rc-service {self.__service} restart', to_stdout=True)

    def rtorrent_clean_lock(self):
        if lxd.get_state(container=self.__container_fullname):
            logger.warning(f'Not cleaning lock on running {self.__container_fullname}')
            return

        lockfile = Path() / self.__container_path_session / 'rtorrent.lock'
        logger.debug(f'Cleaning lock file {lockfile}')
        if Path.exists(lockfile):
            logger.info(f'Removed lockfile {lockfile}')
            lockfile.unlink()

    def rtorrent_clean_torrent(self):
        if self.__container_htpasswd == '1':
            torrent_files_path = Path() / self.__container_path_rushare / 'users' / self.__container_user / 'torrents'
        else:
            torrent_files_path = Path() / self.__container_path_rushare / 'torrents'

        logger.debug(f'Cleaning *.torrent files in {torrent_files_path}')

        for f in torrent_files_path.iterdir():
            if Path.is_file(f) and str(f).endswith('.torrent'):
                f.unlink()

    def update(self):
        if lxd.get_state(container=self.__container_fullname):
            logger.error(f'Not updating running container: {self.__container_fullname}')
            return

        if lxd.get_state(container=self.__container_template):
            # could stop template here but it could be doing something, ie updating
            logger.error(f'Not running update when template is running: {self.__container_template}')
            return

        logger.info(f'Running update for: {self.__container_fullname}')

        check_exists = utils.run_cmd(f'lxc list | grep {self.__container_fullname}',
                                     sh_wrap=True, to_stdout=True)
        if check_exists:
            logger.info(f'Deleting: {self.__container_fullname}')
            utils.run_cmd(f'lxc delete {self.__container_fullname}', to_stdout=True)

        logger.info(f'Copying: {self.__container_template} to {self.__container_fullname}')
        utils.run_cmd(f'lxc copy {self.__container_template} {self.__container_fullname}')

        # removes unneeded access to filesystem on gentoo containers
        logger.info(f'Removing unneeded access to filesystem')
        utils.run_cmd(f'lxc config device remove {self.__container_fullname} distfiles', to_stdout=True)
        utils.run_cmd(f'lxc config device remove {self.__container_fullname} packages', to_stdout=True)
        utils.run_cmd(f'lxc config device remove {self.__container_fullname} repos', to_stdout=True)

        # set cpu/mem limits
        if self.__container_limit_cpu != '0':
            logger.info(f'Setting CPU Limit to {self.__container_limit_cpu}')
            utils.run_cmd(f'lxc config set {self.__container_fullname} '
                          f'limits.cpu {self.__container_limit_cpu}', to_stdout=True)
        if self.__container_limit_cpu_allowance != '0':
            logger.info(f'Setting CPU Allowance Limit to {self.__container_limit_cpu_allowance}')
            utils.run_cmd(f'lxc config set {self.__container_fullname} '
                          f'limits.cpu.allowance {self.__container_limit_cpu_allowance}', to_stdout=True)
        if self.__container_limit_mem != '0':
            logger.info(f'Setting MEM Limit to {self.__container_limit_mem}')
            utils.run_cmd(f'lxc config set {self.__container_fullname} '
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

        utils.run_cmd(f'lxc file push {net_tmp} {net_real}')
        net_tmp.unlink()

        # attach storage dirs to container
        self.attach_dirs()

    def main(self):
        if not Path.is_file(self.__config):
            print('Missing container config file, showing help.\n\n')
            utils.run_cmd(f'{utils.get_script_name()} -H')
            raise SystemExit

        c = 0
        for line in Path.open(self.__config):
            c += 1
            line = line.strip('\n').split(' ')
            if line[0] == 'version':
                if line[1] != self.__CONFIG_VERSION:
                    logger.critical('config versions do not match, update config to new format')
                    raise SystemExit
                continue
            elif line[0] == 'stop':
                logger.trace('will now stop parsing config file')
                raise SystemExit
            elif line[0].startswith('#'):
                logger.trace('Ignoring comment')
                continue
            else:
                try:
                    # test for blank lines, probably
                    # not the best way but it works
                    if line[1] is None:
                        pass
                except IndexError:
                    continue

                try:
                    # set config file variables
                    self.__container_type = line[0]
                    self.__container_distro = line[1]
                    self.__container_user = line[2]
                    self.__container_autostart = line[3]
                    self.__container_htpasswd = line[4]
                    self.__container_ipv4 = line[5]
                    self.__container_limit_cpu = line[6]
                    self.__container_limit_cpu_allowance = line[7]
                    self.__container_limit_mem = line[8]
                    self.__container_name = line[9]
                    try:
                        self.__container_save_override = line[10]
                    except IndexError:
                        self.__container_save_override = None
                except IndexError:
                    logger.critical(f'Malformed config on line {c}')
                    raise SystemExit

                # create actual container name
                self.__container_fullname = f'{self.__container_type}-{self.__container_name}'
                self.__container_template = f'base-{self.__container_distro}-{self.__container_type}'

                if self.__catch_single:
                    if self.__container_fullname != self.__only:
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
                    # self.set_dirs()
                    self.rtorrent_clean_torrent()
                elif self.__print:
                    self.print_config()

    def run(self, args):
        # container
        if args.only:
            self.__only = args.only
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
        if args.edit:
            editor.edit_conf(self.__config)
        if args.cat:
            utils.run_cmd(f'cat {self.__config}')
            raise SystemExit
        if args.print:
            self.__print = True
        if args.print_verbose:
            self.__print = True
            self.__print_verbose = True
        if args.config_help:
            self.config_help()
            raise SystemExit

        self.main()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('-H', '--config-help',
                   action='store_true',
                   help='Show config file help')
    c = p.add_argument_group('CONTAINER')
    c.add_argument('-O', '--only',
                   metavar='CONTAINER',
                   help='Only operate in the supplied container, requires full container name')
    s = p.add_argument_group('CONTAINER SERVICES')
    s.add_argument('-S', '--service',
                   metavar='SERVICE',
                   help='restart service passed as arg')
    s.add_argument('--create-dirs',
                   action='store_true',
                   help='Create container storage dirs if the do not exist')
    g = p.add_argument_group('CONTAINER GENERAL')
    g.add_argument('-d', '--delete',
                   action='store_true',
                   help='Delete containers')
    g.add_argument('-r', '--restart',
                   action='store_true',
                   help='Restart containers')
    g.add_argument('-s', '--start',
                   action='store_true',
                   help='Start containers')
    g.add_argument('-u', '--update',
                   action='store_true',
                   help='Update containers')
    g.add_argument('-z', '--stop',
                   action='store_true',
                   help='Stop containers')
    g.add_argument('-Z', '--force-stop',
                   action='store_true',
                   help='Force stop containers')
    x = p.add_argument_group('SPECIFIC, rutorrent only, no other flags req')
    x.add_argument('-c', '--rutorrent-lockfile',
                   action='store_true',
                   help='rtorrent lockfile cleanup')
    x.add_argument('-C', '--rutorrent-torrents',
                   action='store_true',
                   help='rutorrent cleanup only, remove *.torrent files in $config/rutorrent/share/torrents/')
    o = p.add_argument_group('OTHER')
    o.add_argument('-e', '--edit',
                   action='store_true',
                   help='edit config file')
    o.add_argument('-E', '--cat',
                   action='store_true',
                   help='cat config file')
    o.add_argument('-p', '--print',
                   action='store_true',
                   help='Print all container vars')
    o.add_argument('-P', '--print-verbose',
                   action='store_true',
                   help='Print limited container vars')
    d = p.add_argument_group('DEBUG')
    d.add_argument('-L', '--loglevel',
                   default='INFO',
                   metavar='LEVEL',
                   type=str.upper,
                   choices=['NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'VERBOSE', 'DEBUG', 'TRACE'],
                   help='Levels: %(choices)s')
    args = p.parse_args()

    utils.args_required_else_help()

    logger.remove()
    logger.add(sys.stdout, level=args.loglevel, colorize=True)

    run = Container()
    run.run(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
