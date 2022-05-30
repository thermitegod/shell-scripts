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
# 2022-5-29


import os
from pathlib import Path


def repo_base_dir():
    repo_base_path: str
    while True:
        if (Path.is_dir(Path.cwd() / '.git')):
            repo_base_path = Path.cwd()
            break
        os.chdir('..')

        if (Path.cwd() == '/'):
            print('Failed to find .git')
            raise SystemExit(1)

    return repo_base_path
