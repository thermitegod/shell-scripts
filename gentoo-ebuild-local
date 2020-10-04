#!/usr/bin/env sh
#1.2.0
#2019-03-12

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

die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }

if [ "$(id -u)" -ne 0 ];then die "Requires root";fi

no_live="1"
edit="0"
pkg=""

while getopts "f:lehx" OPT;do
	case "$OPT" in
		l) no_live="0";;
		e) edit="1";;
		f) pkg="${OPTARG}";;
		x) pkg="$(xclip -o)";;
		h)
			printf "GENERAL\n"
			printf " -h\tPrint this help\n"
			printf " -e\tedit ebuild once copied\n"
			printf " -f\tcopy ebuild from gentoo repo to local repo\n"
			printf " -x\tcopy ebuild from gentoo repo to local repo, get pkg from clipboard\n"
			printf " -l\tcopy live ebuild from gentoo repo to local repo\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done
shift $((OPTIND - 1))

repo_location_gentoo="$(grep location /etc/portage/repos.conf/gentoo.conf|awk '{print $3}')"
repo_location_local="$(grep location /etc/portage/repos.conf/local.conf|awk '{print $3}')"

repo_local_path="${repo_location_local}/${pkg}"
repo_gentoo_path="${repo_location_gentoo}/${pkg}"

if [ "$(eix "${pkg}")" = "No matches found" ];then
	die "supplied pkg is invalid: ${pkg}"
fi

if ! [ -d "${repo_local_path}" ];then
	mkdir -pv "${repo_local_path}" || die "mkdir failed"
fi

if [ "${no_live}" = "1" ];then
	pkg_gentoo="$(find "${repo_gentoo_path}" ! -name '*9999*' -name '*.ebuild' 2>/dev/null|sort -V|tail -n1)"
else
	pkg_gentoo="$(find "${repo_gentoo_path}" -name '*.ebuild' 2>/dev/null|sort -V|tail -n1)"
fi

if [ -f "${pkg_gentoo}" ];then
	cp -a "${pkg_gentoo}" "${repo_local_path}" || die "failed to copy ebuild: ${pkg_gentoo}"
else
	die "BUG: selected ebuild does not exist: %s" "${pkg_gentoo}"
fi

if [ -f "${repo_gentoo_path}/metadata.xml" ];then
	cp -a "${repo_gentoo_path}/metadata.xml" "${repo_local_path}" || die "failed to copy metadata.xml"
fi

if [ -d "${repo_gentoo_path}/files" ];then
	cp -av "${repo_gentoo_path}/files" "${repo_local_path}" || die "failed to copy files dir"
fi

if [ "${edit}" = "1" ];then
	"${EDITOR}" "${repo_local_path}"/*.ebuild
fi

cd "${repo_local_path}"
digest-ebuild

