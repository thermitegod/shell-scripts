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
# 2020-12-13


class _Colors:
    def __init__(self):
        super().__init__()

        # reset
        self.NC: str = '\033[0m'

        # regular
        self.BLA: str = '\033[0;30m'
        self.RED: str = '\033[0;31m'
        self.GRE: str = '\033[0;32m'
        self.YEL: str = '\033[0;33m'
        self.BLU: str = '\033[0;34m'
        self.PUR: str = '\033[0;35m'
        self.CYA: str = '\033[0;36m'
        self.WHI: str = '\033[0;37m'

        # bold
        self.BBLA: str = '\033[1;30m'
        self.BRED: str = '\033[1;31m'
        self.BGRE: str = '\033[1;32m'
        self.BYEL: str = '\033[1;33m'
        self.BBLU: str = '\033[1;34m'
        self.BPUR: str = '\033[1;35m'
        self.BCYA: str = '\033[1;36m'
        self.BWHI: str = '\033[1;37m'

        # underline
        self.UBLA: str = '\033[4;30m'
        self.URED: str = '\033[4;31m'
        self.UGRE: str = '\033[4;32m'
        self.UYEL: str = '\033[4;33m'
        self.UBLU: str = '\033[4;34m'
        self.UPUR: str = '\033[4;35m'
        self.UCYA: str = '\033[4;36m'
        self.UWHI: str = '\033[4;37m'

        # high intensity
        self.IBLA: str = '\033[0;90m'
        self.IRED: str = '\033[0;91m'
        self.IGRE: str = '\033[0;92m'
        self.IYEL: str = '\033[0;93m'
        self.IBLU: str = '\033[0;94m'
        self.IPUR: str = '\033[0;95m'
        self.ICYA: str = '\033[0;96m'
        self.IWHI: str = '\033[0;97m'

        # bold high intensity
        self.BIBLA: str = '\033[1;90m'
        self.BIRED: str = '\033[1;91m'
        self.BIGRE: str = '\033[1;92m'
        self.BIYEL: str = '\033[1;93m'
        self.BIBLU: str = '\033[1;94m'
        self.BIPUR: str = '\033[1;95m'
        self.BICYA: str = '\033[1;96m'
        self.BIWHI: str = '\033[1;97m'

        # background
        self.ON_BLA: str = '\033[40m'
        self.ON_RED: str = '\033[41m'
        self.ON_GRE: str = '\033[42m'
        self.ON_YEL: str = '\033[43m'
        self.ON_BLU: str = '\033[44m'
        self.ON_PUR: str = '\033[45m'
        self.ON_CYA: str = '\033[46m'
        self.ON_WHI: str = '\033[47m'

        # high intensity backgrounds
        self.ON_IBLA: str = '\033[0;100m'
        self.ON_IRED: str = '\033[0;101m'
        self.ON_IGRE: str = '\033[0;102m'
        self.ON_IYEL: str = '\033[0;103m'
        self.ON_IBLU: str = '\033[0;104m'
        self.ON_IPUR: str = '\033[0;105m'
        self.ON_ICYA: str = '\033[0;106m'
        self.ON_IWHI: str = '\033[0;107m'


Colors = _Colors()
