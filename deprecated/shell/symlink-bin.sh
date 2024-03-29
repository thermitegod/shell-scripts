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
# 2.2.0
# 2019-05-17


die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }

ignore="--ignore=".git" --ignore=".gitignore""

B="/home/brandon"
c="${B}/.config"
h="${B}/.bin"

if [ -z "${1}" ];then "${0}" -h;exit;fi
while getopts "BPRbprh" OPT;do
	case "$OPT" in
		b) cd "$h" || die;doas stow "$ignore" -v --target=/usr/local/bin bin bin-other opt;;
		B) cd "$h" || die;doas stow "$ignore" -D -v --target=/usr/local/bin bin bin-other opt;;
		p) cd "$c" || die;stow "$ignore" -v --target="${B}" shell;;
		P) cd "$c" || die;stow "$ignore" -D -v --target="${B}" shell;;
		r) cd "$c" || die;doas stow "$ignore" -v --target=/root shell;;
		R) cd "$c" || die;doas stow "$ignore" -D -v --target=/root shell;;
		h)
			printf "STOW\n"
			printf " -b\tstow files in %s/.bin/bin{-other},opt to /usr/local/bin\n" "${B}"
			printf " -p\tstow files in %s/shell to %s\n" "${c}" "${B}"
			printf " -r\tstow files in %s/shell to /root\n" "${c}"
			printf "\nUNSTOW\n"
			printf " -B\tunstow files in %s/.bin/bin{-other},opt in /usr/local/bin\n" "${B}"
			printf " -P\tunstow files in %s/shell in %s\n" "${c}" "${B}"
			printf " -R\tunstow files in %s/shell in /root\n" "${c}"
			printf "\nGENERAL\n"
			printf " -h\tprint this help\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done
