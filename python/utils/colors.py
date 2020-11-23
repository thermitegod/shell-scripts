# -*- coding: utf-8 -*-
# 1.1.1
# 2020-11-22

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


class _Colors:
    def __init__(self):
        super().__init__()

        # reset
        self.NC = '\033[0m'

        # regular
        self.BLA = '\033[0;30m'
        self.RED = '\033[0;31m'
        self.GRE = '\033[0;32m'
        self.YEL = '\033[0;33m'
        self.BLU = '\033[0;34m'
        self.PUR = '\033[0;35m'
        self.CYA = '\033[0;36m'
        self.WHI = '\033[0;37m'

        # bold
        self.BBLA = '\033[1;30m'
        self.BRED = '\033[1;31m'
        self.BGRE = '\033[1;32m'
        self.BYEL = '\033[1;33m'
        self.BBLU = '\033[1;34m'
        self.BPUR = '\033[1;35m'
        self.BCYA = '\033[1;36m'
        self.BWHI = '\033[1;37m'

        # underline
        self.UBLA = '\033[4;30m'
        self.URED = '\033[4;31m'
        self.UGRE = '\033[4;32m'
        self.UYEL = '\033[4;33m'
        self.UBLU = '\033[4;34m'
        self.UPUR = '\033[4;35m'
        self.UCYA = '\033[4;36m'
        self.UWHI = '\033[4;37m'

        # high intensity
        self.IBLA = '\033[0;90m'
        self.IRED = '\033[0;91m'
        self.IGRE = '\033[0;92m'
        self.IYEL = '\033[0;93m'
        self.IBLU = '\033[0;94m'
        self.IPUR = '\033[0;95m'
        self.ICYA = '\033[0;96m'
        self.IWHI = '\033[0;97m'

        # bold high intensity
        self.BIBLA = '\033[1;90m'
        self.BIRED = '\033[1;91m'
        self.BIGRE = '\033[1;92m'
        self.BIYEL = '\033[1;93m'
        self.BIBLU = '\033[1;94m'
        self.BIPUR = '\033[1;95m'
        self.BICYA = '\033[1;96m'
        self.BIWHI = '\033[1;97m'

        # background
        self.ON_BLA = '\033[40m'
        self.ON_RED = '\033[41m'
        self.ON_GRE = '\033[42m'
        self.ON_YEL = '\033[43m'
        self.ON_BLU = '\033[44m'
        self.ON_PUR = '\033[45m'
        self.ON_CYA = '\033[46m'
        self.ON_WHI = '\033[47m'

        # high intensity backgrounds
        self.ON_IBLA = '\033[0;100m'
        self.ON_IRED = '\033[0;101m'
        self.ON_IGRE = '\033[0;102m'
        self.ON_IYEL = '\033[0;103m'
        self.ON_IBLU = '\033[0;104m'
        self.ON_IPUR = '\033[0;105m'
        self.ON_ICYA = '\033[0;106m'
        self.ON_IWHI = '\033[0;107m'


Colors = _Colors()
