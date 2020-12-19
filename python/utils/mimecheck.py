# -*- coding: utf-8 -*-
# 1.5.0
# 2020-12-13

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
from pathlib import Path
from typing import Union

from python.utils.execute import Execute


class _Mimecheck:
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_mimetype_ext(filename: Union[Path, str]):
        mime = Execute(f'file -b --mime-type -- "{filename}"', to_stdout=True).get_out()
        return mime.strip('\n').split('/')[1]

    def check_if_video(self, filename: Union[Path, str]):
        return self.__check_mimetype(filename=filename, mime_type='video')

    def check_if_audio(self, filename: Union[Path, str]):
        return self.__check_mimetype(filename=filename, mime_type='audio')

    def check_if_image(self, filename: Union[Path, str]):
        return self.__check_mimetype(filename=filename, mime_type='image')

    @staticmethod
    def __check_mimetype(filename: Union[Path, str], mime_type: str):
        try:
            if mime_type in mimetypes.guess_type(str(filename))[0]:
                return True
        except TypeError:
            pass
        return False


Mimecheck = _Mimecheck()
