#!/usr/bin/env python3
# 1.0.0
# 2020-05-06

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

from utils import utils


def main():
    print('Current tmux sessions\n')
    print('===================')
    utils.run_cmd('tmux list-session -F \'#S\'')
    print('===================\n')
    session = input('Enter session name to connect: ')
    utils.run_cmd(f'tmux attach -t {session}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
