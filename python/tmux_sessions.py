# -*- coding: utf-8 -*-
# 1.1.0
# 2020-11-11

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

from python.utils import utils


def main():
    print('Current tmux sessions\n')
    print('===================')
    utils.run_cmd('tmux list-session -F \'#S\'')
    print('===================\n')
    session = input('Enter session name to connect: ')
    utils.run_cmd(f'tmux attach -t {session}')
