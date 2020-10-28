# -*- coding: utf-8 -*-
# 1.0.0
# 2020-10-28

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

from . import utils


class _Script:
    def __init__(self):
        super().__init__()
        atexit.register(self.remove_tmpdir)

        self.__tmpdir = Path(tempfile.mkdtemp())

        self.__script = Path() / self.__tmpdir / 'tmp.sh'

    def remove_tmpdir(self):
        shutil.rmtree(self.__tmpdir)

    def execute_script_shell(self, text: str, execute_script: bool = True):
        """
        :param text:
            Text of the shell script
        :param execute_script:
            execute script after writing
        """

        script = '#!/usr/bin/env sh\n' \
                 f'die(){{ /bin/echo -e $*;kill {os.getpid()};exit; }}\n' \
                 f'{text}\n'

        self.__script.write_text(script)
        Path.chmod(self.__script, 0o700)

        if execute_script:
            utils.run_cmd(str(self.__script))

            # some scripts will generate multiple shell scripts
            # and these need to be removed after each run
            Path.unlink(self.__script)


Script = _Script()
