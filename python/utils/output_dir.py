# -*- coding: utf-8 -*-
# 1.0.0
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

from pathlib import Path


def set_output_dir(directory: list):
    out = Path.resolve(Path(directory[0]))

    if not Path.is_dir(out):
        if Path.exists(out):
            print(f'selected output dir \'{out}\' exists but is not a directory')
            raise SystemExit(1)
        out.mkdir(parents=True, exist_ok=True)

    return out
