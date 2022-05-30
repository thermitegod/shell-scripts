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
# 2020-10-10


import os
from pathlib import Path


def get_home_dir():
    return Path() / os.environ['HOME']


def get_config_dir():
    return Path() / os.environ['XDG_CONFIG_HOME']


def get_data_dir():
    return Path() / os.environ['XDG_DATA_HOME']


def get_download_dir():
    return Path() / os.environ['XDG_DOWNLOAD_DIR']
