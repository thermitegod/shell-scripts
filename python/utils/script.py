# Copyright (C) 2018-2023 Brandon Zorn <brandonzorn@cock.li>
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
# 3.0.0
# 2023-03-31


import atexit
import os
import shutil
import tempfile
from pathlib import Path

from utils.execute import Execute


class ExecuteBashScript:
    def __init__(self, cmd: str):
        """
        Writes the contents of cmd to a a file and executes it.
        reasons to use this over Execute(); setting env variables,
        complex shell logic, error handling in the shell code,
        using >| or >>|, etc ...

        includes 'die' function to kill the invoking script,
        example 'ls /path/does/not/exist || die "error message"'

        :param cmd:
            shell code to be written and executed
        """

        super().__init__()

        atexit.register(self._remove_tmpdir)
        self.__tmpdir: Path = Path(tempfile.mkdtemp())

        script_file: Path = Path() / self.__tmpdir / 'exec.bash'
        script: str = f'#!/usr/bin/env bash\n\n' \
                      f'die() {{\n' \
                      f'    echo -e $*\n' \
                      f'    kill {os.getpid()}\n' \
                      f'    exit\n' \
                      f'}}\n\n' \
                      f'{cmd}\n'

        script_file.write_text(script)
        Path.chmod(script_file, 0o700)

        Execute(str(script_file))

    def _remove_tmpdir(self):
        shutil.rmtree(self.__tmpdir)

class ExecuteFishScript:
    def __init__(self, cmd: str):
        """
        Writes the contents of cmd to a a file and executes it.
        reasons to use this over Execute(); setting env variables,
        complex shell logic, error handling in the shell code,
        using >| or >>|, etc ...

        includes 'die' function to kill the invoking script,
        example 'ls /path/does/not/exist || die "error message"'

        :param cmd:
            shell code to be written and executed
        """

        super().__init__()

        atexit.register(self._remove_tmpdir)
        self.__tmpdir: Path = Path(tempfile.mkdtemp())

        script_file: Path = Path() / self.__tmpdir / 'exec.fish'
        script: str = f'#!/usr/bin/env fish\n\n' \
                      f'function die\n' \
                      f'    command echo -e $argv\n' \
                      f'    kill {os.getpid()}\n' \
                      f'    exit\n' \
                      f'end\n\n' \
                      f'{cmd}\n'

        script_file.write_text(script)
        Path.chmod(script_file, 0o700)

        Execute(str(script_file))

    def _remove_tmpdir(self):
        shutil.rmtree(self.__tmpdir)
