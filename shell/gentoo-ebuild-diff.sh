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
# 1.3.0
# 2020-03-12


die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }

no_live="1"
diff_mode="gentoo_local"
pkg=""

if [ -z "${1}" ];then "${0}" -h;exit;fi
while getopts "f:Iilhrx" OPT;do
	case "$OPT" in
		I) diff_mode="installed_gentoo";;
		i) diff_mode="installed_local";;
		r) diff_mode="local_gentoo";;
		l) no_live="0";;
		f) pkg="${OPTARG}";;
		x) pkg="$(xclip -o)";;
		h)
			printf "GENERAL\n"
			printf " -h\tPrint this help\n"
			printf " -f\tget pkg from \$1\n"
			printf " -I\tdiff installed against gentoo repo\n"
			printf " -i\tdiff installed against local repo\n"
			printf " -l\tenable diffing live ebuild, otherwise ignores them\n"
			printf " -r\tdiff 'local gentoo' instead of 'gentoo local'\n"
			printf " -x\tget pkg from clipboard\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done
#shift $((OPTIND - 1))

repo_location_gentoo="$(grep location /etc/portage/repos.conf/gentoo.conf|awk '{print $3}')"
repo_location_local="$(grep location /etc/portage/repos.conf/local.conf|awk '{print $3}')"
repo_location_installed="/var/db/pkg"

repo_local_path="${repo_location_local}/${pkg}"
repo_gentoo_path="${repo_location_gentoo}/${pkg}"
repo_installed_path="${repo_location_installed}/${pkg}"

if [ "$(eix "${pkg}")" = "No matches found" ];then
	die "supplied pkg is invalid: ${pkg}"
fi

if [ "${no_live}" = "1" ];then
	pkg_gentoo="$(find "${repo_gentoo_path}" ! -name '*9999*' -name '*.ebuild' 2>/dev/null|sort -V|tail -n1)"
	pkg_local="$(find "${repo_local_path}" ! -name '*9999*' -name '*.ebuild' 2>/dev/null|sort -V|tail -n1)"
else
	pkg_gentoo="$(find "${repo_gentoo_path}" -name '*.ebuild' 2>/dev/null|sort -V|tail -n1)"
	pkg_local="$(find "${repo_local_path}" -name '*.ebuild' 2>/dev/null|sort -V|tail -n1)"
fi

pkg_installed="$(find ${repo_installed_path}* -name '*.ebuild' 2>/dev/null)"

case "${diff_mode}" in
	gentoo_local)
		diff_old="${pkg_gentoo}"
		diff_new="${pkg_local}"
		;;
	local_gentoo)
		diff_old="${pkg_local}"
		diff_new="${pkg_gentoo}"
		;;
	installed_local)
		diff_old="${pkg_installed}"
		diff_new="${pkg_local}"
		;;
	installed_gentoo)
		diff_old="${pkg_installed}"
		diff_new="${pkg_gentoo}"
		;;
esac

if ! [ -f "${diff_old}" ] || ! [ -f "${diff_new}" ];then die "No ebuilds found for: ${pkg}";fi

if [ "$(openssl sha1 "${diff_old}"|awk '{print $2}')" = "$(openssl sha1 "${diff_new}"|awk '{print $2}')" ];then
	printf "these ebuilds are the same: \n${diff_old}\n${diff_new}\n"
	exit
else
	diff -Naur "${diff_old}" "${diff_new}"
fi

