# -*- coding: utf-8 -*-
# 1.0.0
# 2020-09-24

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

import mimetypes


def check_if_video(filename: str):
    try:
        if 'video' in mimetypes.guess_type(filename)[0]:
            return True
    except TypeError:
        pass
    return False


def check_if_audio(filename: str):
    try:
        if 'audio' in mimetypes.guess_type(filename)[0]:
            return True
    except TypeError:
        pass
    return False
