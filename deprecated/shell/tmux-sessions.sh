#!/usr/bin/env sh

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
# 3.1.0
# 2019-05-17


wip()
{

user=$(id -u)
if ! [ -S "/tmp/tmux-${user}/default" ];then
	printf "No tmux sessions exist for uid %s\n" "${user}"
	exit
fi

if [ -z "${1}" ];then
	printf "Current tmux sessions\nEnter session name to connect\n"
	read -r s
else
	s="${1}"
fi
tmux attach -t "${s}"

}

#printf "to attach: tmux attach -t <session>\n\n"
printf "Current tmux sessions\n"
printf "Enter session name to connect\n"
tmux list-session -F '#S'
read -r tsession
tmux attach -t "${tsession}"
