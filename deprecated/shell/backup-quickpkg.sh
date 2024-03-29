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
# 4.9.0
# 2019-09-25


#repos dir has
#/var/db/repos/{gentoo,local,layman}

die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }
if [ "$(id -u)" -ne 0 ];then die "Requires root, exiting.";fi
finish(){ if [ -d "${tmpdir}" ];then rm --preserve-root -r "${tmpdir}";fi }
trap 'exit 1' INT HUP QUIT TERM USR1
trap finish EXIT
tmpdir=$(mktemp -d)
chmod 755 "$tmpdir"

comp()
{
	target_zst="${date}-${name}.tar.${E}"
	target_dest="${data}/${name}"
	if ! [ -d "${target_dest}" ];then mkdir -p "${target_dest}";fi
	tar --xattrs --sparse -${V}cf - "${target_dir}" -P | "$C" "$A" >| "${tmpdir}/${target_zst}"
	chown -R "${user}:${group}" "${tmpdir}"
	mv -i "${tmpdir}/${target_zst}" "${target_dest}"
}

date=$(date +%F-%H%M)
user="brandon"
group="${user}"
data="/mnt/data/backup/gentoo"
mode="z"
comp="zstd"
V=""

if [ -z "${1}" ];then "${0}" -h;exit;fi
while getopts "1234ahvxz" OPT;do
	case "$OPT" in
		1) mode="packages";;
		2) mode="repos";;
		3) mode="portage_etc";;
		4) mode="portage_world";;
		a) mode="all";;
		v) V="v";;
		x) comp="xz";;
		z) comp="zstd";;
		h)
			printf "\nGENERAL\n"
			printf " -h\tprint this help\n"
			printf " -v\tverbose\n"
			printf " -x\tuse xz\n"
			printf " -z\tuse zstd\n"
			printf "\nCOMPRESS\n"
			printf " -a\teverything\n"
			printf " -1\tpackages\n"
			printf " -2\trepos\n"
			printf " -3\tportage etc\n"
			printf " -4\tportage world\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

case "${comp}" in
	zstd) C="zstd";A="-T0";E="zst";;
	xz) C="xz";A="-e9";E="xz";;
esac

case ${mode} in
	packages)
		target_dest="${data}/packages"
		if ! [ -d "${target_dest}" ];then mkdir -p "${target_dest}";fi
		work="${tmpdir}/packages-${date}"
		mkdir "${work}"
		export PKGDIR="${work}"
		quickpkg --include-config=y "*/*"
		chown -R "${user}:${group}" "${tmpdir}"
		mv -i "${work}" "${target_dest}"
		;;
	repos)
		name="repos"
		target_dir="/var/db/repos"
		comp
		;;
	portage_etc)
		name="portage-etc"
		target_dir="/etc/portage"
		comp
		;;
	portage_world)
		name="portage-world"
		target_dir="/var/lib/portage"
		comp
		;;
	all)
		"$0" -2 &
		"$0" -3 &
		"$0" -4 &
		"$0" -1
		;;
esac
