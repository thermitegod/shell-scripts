#!/usr/bin/env python3

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
# 1.2.0
# 2020-11-11


from pathlib import Path

from utils.colors import Colors


def main():
    vuln = Path() / '/sys/devices/system/cpu/vulnerabilities'

    for f in Path(vuln).iterdir():
        name = f.name
        state = (f.read_text().strip('\n'))
        print(f'{Colors.YEL}{name: >20}{Colors.NC} : {state}')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
