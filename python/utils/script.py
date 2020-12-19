# -*- coding: utf-8 -*-
# 2.1.0
# 2020-12-13

# Copyright (C) 2019,2020 Brandon Zorn <brandonzorn@cock.li>
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

import atexit
import os
import shutil
import tempfile
from pathlib import Path

from python.utils.execute import Execute


class ExecuteScript:
    def __init__(self, cmd: str):
        """
        Writes the contents of cmd to a a file and executes it.
        reasons to use this over Execute(); setting env variables,
        complex shell logic, error handeling in the shell code,
        using >| or >>|, etc ...

        includes 'die' function to kill the invoking script,
        example 'ls /doesnotexist || die "retard"'

        :param cmd:
            shell code to be written and executed
        """

        super().__init__()

        atexit.register(self._remove_tmpdir)
        self.__tmpdir: Path = Path(tempfile.mkdtemp())

        script_file: Path = Path() / self.__tmpdir / 'tmp.sh'
        script: str = '#!/usr/bin/env sh\n' \
                      f'die(){{ /bin/echo -e $*;kill {os.getpid()};exit; }}\n' \
                      f'{cmd}\n'

        script_file.write_text(script)
        Path.chmod(script_file, 0o700)

        Execute(str(script_file))

    def _remove_tmpdir(self):
        shutil.rmtree(self.__tmpdir)
