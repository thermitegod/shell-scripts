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
# 1.4.1
# 2019-07-15


die(){ /bin/echo -e "$*";exit 1; }
if [ "$(id -u)" -ne 0 ];then die "Requires root, exiting";fi

. "$(dirname "$0")/colors.sh"

tape="/dev/st0"

t_rewind(){ mt -f "$tape" rewind; }
t_status(){ mt -f "$tape" status; }
t_reten(){ mt -f "$tape" retension; }
t_eject(){ mt -f "$tape" eject; }
t_erase(){ mt -f "$tape" erase; }

t_list(){ tar -tf "${tape}"; }

t_cdloc()
{
	#dont tar unneeded paths
	if [ -d "${target}" ];then
		cd "${target}/.." || die
	elif [ -f "${target}" ];then
		target="$(dirname "${target}")"
		cd "${target}" || die
	else
		printf "not a file or directory\n"
	fi
}

t_confirm_erase()
{
	read -r -p "Confirm erase current tape [yn]? " confirm
	if echo "${confirm}" | grep -iq "^y" ;then
		t_erase
	else
		die "Exiting. Did not enter: y"
	fi
}

t_backup()
{
	if [ -z "${target}" ];then die "nothing to backup, exiting";fi
	t_cdloc

	#move to end last tar on tape
	#mt -f "${tape}" eom
	mt -f "${tape}" eod
	tar -cvf "${tape}" "${target}"
}

t_backup_overwrite()
{
	if [ -z "${target}" ];then die "nothing to backup, exiting";fi
	t_cdloc
	t_rewind
	tar -cvf "${tape}" "${target}"
}

t_restore()
{
	if [ -z "${target}" ];then die "no restore target specified, exiting";fi
	t_rewind
	tar -xvf /dev/st0 -C "${target}"
}

t_verify()
{
	t_rewind
	tar -tvf "${tape}"
}

if [ -z "${1}" ];then "${0}" -h;exit;fi
while getopts "B:b:eg:hHlRrsvZz" OPT;do
	case "$OPT" in
		b) target="$OPTARG";t_backup;;
		B) target="$OPTARG";t_backup_overwrite;;
		e) t_eject;;
		g) target="$OPTARG";t_restore;;
		l) t_list;;
		R) t_reten;;
		r) t_rewind;;
		s) t_status;;
		v) t_verify;;
		z) t_confirm_erase;t_rewind;;
		Z) t_confirm_erase;t_rewind;t_eject;;
		h)
			printf "\nTAPE\n"
			printf " Tape drive is : %s\n" "${tape}"
			printf " -b\tbackup \$1 at end of last backup on %s\n" "${tape}"
			printf " -B\tbackup \$1 at start, overwriting existing, on %s\n" "${tape}"
			printf " -e\teject tape\n"
			printf " -g\trestore from begining of %s to \$1\n" "${tape}"
			printf " -l\tlist contents of %s\n" "${tape}"
			printf " -r\trewind tape\n"
			printf " -R\ttape retensioning <only for tape read errors>\n"
			printf " -s\tdrive status\n"
			printf " -v\tverify files on current tape\n"
			printf " -z\terase/rewind tape\n"
			printf " -Z\terase/rewind/eject tape\n"
			printf "\nGENERAL\n"
			printf " -h\tPrint this help\n"
			printf " -H\tprint web links\n"
			exit;;
		H)
			printf "https://www.cyberciti.biz/hardware/unix-linux-basic-tape-management-commands\n"
			printf "https://www.cyberciti.biz/faq/unix-verify-tape-backup\n"
			printf "https://www.cyberciti.biz/faq/linux-tape-backup-with-mt-and-tar-command-howto\n"
			printf "https://community.hpe.com/t5/StoreEver-Tape-Storage/determining-free-space-on-tape-under-Linux/td-p/3624568\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done
shift $((OPTIND - 1))

