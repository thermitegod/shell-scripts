# -*- coding: utf-8 -*-
# 4.5.0
# 2020-11-21

# Copyright (C) 2018,2019,2020 Brandon Zorn <brandonzorn@cock.li>
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


import time
from pathlib import Path

from python.utils import utils
from python.utils.execute import Execute


def main():
    cmd = 'gm import '

    if utils.get_script_name() == 'snip-root':
        cmd += '-window root '

    cmd += f'{Path.home()}/{int(time.time())}.png'

    Execute(cmd)
