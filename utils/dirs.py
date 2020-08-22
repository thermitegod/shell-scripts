# -*- coding: utf-8 -*-
# 1.0.0
# 2020-08-21

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

import os
from pathlib import Path


def get_home_dir():
    return Path() / os.environ['HOME']


def get_config_dir():
    return Path() / os.environ['XDG_CONFIG_HOME']


def get_data_dir():
    return Path() / os.environ['XDG_DATA_HOME']


def get_extra_dir():
    return Path() / os.environ['XDG_DATA_HOME'] / 'shell'
