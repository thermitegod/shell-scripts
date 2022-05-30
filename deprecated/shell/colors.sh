#!/usr/bin/env sh

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
# 1.0.0
# 2019-01-17


#reset
NC="\033[0m"

#regular
BLA="\033[0;30m"
RED="\033[0;31m"
GRE="\033[0;32m"
YEL="\033[0;33m"
BLU="\033[0;34m"
PUR="\033[0;35m"
CYA="\033[0;36m"
WHI="\033[0;37m"

#bold
BBLA="\033[1;30m"
BRED="\033[1;31m"
BGRE="\033[1;32m"
BYEL="\033[1;33m"
BBLU="\033[1;34m"
BPUR="\033[1;35m"
BCYA="\033[1;36m"
BWHI="\033[1;37m"

#underline
UBLA="\033[4;30m"
URED="\033[4;31m"
UGRE="\033[4;32m"
UYEL="\033[4;33m"
UBLU="\033[4;34m"
UPUR="\033[4;35m"
UCYA="\033[4;36m"
UWHI="\033[4;37m"

#high intensity
IBLA="\033[0;90m"
IRED="\033[0;91m"
IGRE="\033[0;92m"
IYEL="\033[0;93m"
IBLU="\033[0;94m"
IPUR="\033[0;95m"
ICYA="\033[0;96m"
IWHI="\033[0;97m"

#bold high intensity
BIBLA="\033[1;90m"
BIRED="\033[1;91m"
BIGRE="\033[1;92m"
BIYEL="\033[1;93m"
BIBLU="\033[1;94m"
BIPUR="\033[1;95m"
BICYA="\033[1;96m"
BIWHI="\033[1;97m"

#background
ON_BLA="\033[40m"
ON_RED="\033[41m"
ON_GRE="\033[42m"
ON_YEL="\033[43m"
ON_BLU="\033[44m"
ON_PUR="\033[45m"
ON_CYA="\033[46m"
ON_WHI="\033[47m"

#high intensity backgrounds
ON_IBLA="\033[0;100m"
ON_IRED="\033[0;101m"
ON_IGRE="\033[0;102m"
ON_IYEL="\033[0;103m"
ON_IBLU="\033[0;104m"
ON_IPUR="\033[0;105m"
ON_ICYA="\033[0;106m"
ON_IWHI="\033[0;107m"
