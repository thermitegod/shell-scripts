#!/usr/bin/env sh
#1.3.0
#2019-05-27

# Copyright (C) 2018,2019 Brandon Zorn <brandonzorn@cock.li>
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

#not really portable, more qol

#TODO
#flags
#everything else
#will take backbone of lxd-admin for state checking and other qol things
#make /root/setup-* in this script and push to container

printf "Stoping master\n"
lxc stop dev-gentoo-clang-minimal

printf "stoping subs\n"
lxc stop base-gentoo-rutorrent
lxc stop base-gentoo-transmission

printf "deleting subs\n"
lxc delete base-gentoo-rutorrent
lxc delete base-gentoo-transmission

printf "copying master to subs\n"
lxc copy dev-gentoo-clang-minimal base-gentoo-rutorrent
lxc copy dev-gentoo-clang-minimal base-gentoo-transmission

printf "starting subs\n\n"
lxc start base-gentoo-rutorrent
lxc start base-gentoo-transmission

sleep 2

read -p "rutorrent, enter to continue: " z;unset z
lxc exec base-gentoo-rutorrent /root/setup-rutorrent.sh

printf "\n"

read -p "transmission, enter to continue: " z;unset z
lxc exec base-gentoo-transmission /root/setup-transmission.sh

sleep 2

printf "stoping subs\n"
lxc stop base-gentoo-rutorrent
lxc stop base-gentoo-transmission

printf "Done\n"

