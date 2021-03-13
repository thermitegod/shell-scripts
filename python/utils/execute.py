# -*- coding: utf-8 -*-
# 1.6.0
# 2021-03-13

# Copyright (C) 2019,2020,2021 Brandon Zorn <brandonzorn@cock.li>
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

import shlex
import subprocess


class Execute:
    def __init__(self, cmd: str, *, sh_wrap: bool = False,
                 to_stdout: bool = False, shell: bool = False,
                 blocking: bool = True):
        """
        :param cmd:
            shell command to run
        :param sh_wrap:
            wrap command in 'sh -c ""', required if using pipes
        :param to_stdout:
            send output to stdout, required if using get_out().
            Can also be used to silence command output.
        :param shell:
            use subprocess arg shell=True
        :param blocking:
            use a non blocking version of subprocess, ignores to_stdout
        """

        super().__init__()

        self.__cmd: str = cmd
        self.__out: str = ''

        if sh_wrap:
            self.__cmd = f'sh -c "{self.__cmd}"'

        self.__cmd = shlex.split(self.__cmd)

        if not blocking:
            subprocess.Popen(self.__cmd,
                             stdout=subprocess.PIPE,
                             shell=shell,
                             start_new_session=True)
            return

        if to_stdout:
            out = subprocess.run(self.__cmd,
                                 stdout=subprocess.PIPE,
                                 shell=shell)
            self.__out = out.stdout.decode('utf-8')
        else:
            # need to use to_stdout to get the generated output,
            # will return none if get_out() is used instead of ''
            # when tyring to assign to self.__out
            subprocess.run(self.__cmd)

    def get_out(self):
        return self.__out
