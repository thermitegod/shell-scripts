#!/usr/bin/env python3
# 1.1.2
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

import shutil
import datetime
from pathlib import Path


def main():
    time = datetime.datetime.now()
    year = str(time.year)
    month = str(time.month)
    day = str(time.day)

    db = 'vnstat.db'
    target_src = Path() / '/var/lib/vnstat' / db
    target_dst = Path() / '/mnt/data/backup/vnstat-database' / year / month / day / db

    target_dst.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(target_src, target_dst)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
