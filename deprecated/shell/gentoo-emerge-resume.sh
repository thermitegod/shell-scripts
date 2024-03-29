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
# 5.7.0
# 2019-05-17


die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }
finish(){ if [ -d "${tmpdir}" ];then rm --preserve-root -r "${tmpdir}";fi }
trap 'exit 1' INT HUP QUIT TERM USR1
trap finish EXIT
tmpdir=$(mktemp -d)
chmod 755 "${tmpdir}"

bac()
{
	if ! [ -d "${storage}" ];then mkdir -p "${storage}" && chown "${user}:${group}" "${storage}";fi
	cp "${mtimedb}" "${tmpdir}"
	zstd "${tmpdir}/mtimedb"
	mv "${tmpdir}/${mtime_zst}" "${storage}/${date}-${mtime_zst}"
	chown "${user}:${group}"  "${storage}/${date}-${mtime_zst}"
	printf "Finished backup of %s to %s\n" "${date}-${mtime_zst}" "${storage}"
}

res()
{
	if [ -z "$(ls -1A "${storage}" 2>/dev/null)" ];then die "Run a backup first. Exiting.";fi
	#if ! [ -d "$storage" ];then die "Run a backup first. Exiting.";fi
	if [ "${res_specific}" = "1" ];then
		printf "Selected mtimedb to restore\n"
		printf "==MUST== input full name\n"
		ls -1A "$storage"
		printf "\n"
		read -r mtime_res
	else
		mtime_res=$(ls -1A "${storage}"|tail -n1)
	fi

	cp "${storage}/${mtime_res}" "${tmpdir}"
	unzstd "${tmpdir}/${mtime_res}"
	mv "${tmpdir}/${mtime_res%%.*}" "${tmpdir}/mtimedb" #removes date prefix
	if [ -f "${mtimedb}" ];then rm "${mtimedb}";fi
	mv "${tmpdir}/mtimedb" "${mtimedb}"
	printf "Finished restore of %s to %s\n" "${mtime_res}" "${mtimedb}"
}

res_specific="0"
date=$(date "+%F-%s")
storage="/mnt/data/backup/mtimedb"
mtimedb="/var/cache/edb/mtimedb"
mtime_zst="mtimedb.zst"
user="brandon"
group="$user"

if [ -z "${1}" ];then "${0}" -h;exit;fi
while getopts "brsldh" OPT;do
	case "$OPT" in
		b) bac;;
		#r) res_specific="0";res;;
		r) die "Disabled, use -s";;
		s) res_specific="1";res;;
		l)
			if ! [ -d "${storage}" ];then die "Run a backup first. Exiting.";fi
			printf "Listing files in : %s\n" "${storage}"
			ls -1A ${storage}
			;;
		d)
			if [ -d "${storage}" ];then
				rm -rfv "${storage}" || die
			else
				printf "Nothing to delete\n"
			fi
			;;
		h)
			printf " -b\tbackup\n"
			printf " -r\trestore last <wip>\n"
			printf " -s\trestore selected\n"
			printf " -l\tlist\n"
			printf " -d\tdelete\n"
			printf " -h\tprint this help\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done
