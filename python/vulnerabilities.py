#!/usr/bin/env python3
# 1.0.0
# 2020-09-19

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


from pathlib import Path

from utils import colors


def main():
    vuln = Path() / '/sys/devices/system/cpu/vulnerabilities'

    c = colors.Colors

    for f in Path(vuln).iterdir():
        name = f.name
        state = (f.read_text().strip('\n'))
        print(f'{c.YEL}{name: >20}{c.NC} : {state}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
