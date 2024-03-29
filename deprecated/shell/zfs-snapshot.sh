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
# 4.1.0
# 2019-09-25


S="manual-$(date +%F-%H%M)"
ZFS="/sbin/zfs"

if [ -z "${1}" ];then "${0}" -h;exit;fi
while getopts "m:B:acsudlh" OPT;do
	case "$OPT" in
		m)
			case "$OPTARG" in
				1) "$ZFS" snapshot -r "zroot/ROOT/gentoo@${S}";;
				2) "$ZFS" snapshot -r "zroot/HOME/brandon@${S}";;
				3) "$ZFS" snapshot -r "storage/anime@${S}";;
				4) "$ZFS" snapshot -r "storage/data@${S}";;
				5) "$ZFS" snapshot -r "ssd-mirror/KVM@${S}";;
				6) "$ZFS" snapshot -r "torrents@${S}";;
				7) "$ZFS" snapshot -r "zroot/CACHE/torrents@${S}";;
			esac;;
		B) "$ZFS" send "${OPTARG}" | zstd -T0 >| "${OPTARG##*/}.zst";;
		a) "$ZFS" list -t snapshot;;
		c)
			"$ZFS" list -t snapshot \
				zroot/CACHE/torrents
			;;
		s)
			"$ZFS" list -t snapshot \
				ssd-mirror/MUSIC \
				ssd-mirror/KVM
			;;
		u)
			"$ZFS" list -t snapshot \
				zroot/HOME/brandon \
				zroot/HOME/root \
				zroot/HOME/sandbox
			;;
		d)
			"$ZFS" list -t snapshot \
				storage/data \
				storage/anime \
				torrents
			;;
		l)
			"$ZFS" list -t snapshot \
				zroot/ROOT/gentoo \
				zroot/ROOT/gentoo/var
			;;
		h)
			printf "GENERAL\n"
			printf " -h\tprint this help\n"
			printf "\nSNAPSHOT PRINTING\n"
			printf " -a\tprint all snapshots\n"
			printf " -d\tprint snapshots of storage/{anime,data} and torrents\n"
			printf " -c\tprint snapshots of zroot/CACHE/torrents\n"
			printf " -s\tprint snapshots of ssd-mirror/{MUSIC,KVM}\n"
			printf " -u\tprint snapshots of zroot/HOME/*\n"
			printf " -l\tprint snapshots of zroot/ROOT/gentoo{/var,/var/log}\n"
			printf "\nDATASET SNAPSHOTS\n"
			printf "\tformat: pool/dataset@%s\n\n" "${S}"
			printf " -m {1..7}\n"
			printf "\t1 :zroot/ROOT/gentoo\n"
			printf "\t2 :zroot/HOME/brandon\n"
			printf "\t3 :storage/anime\n"
			printf "\t4 :storage/data\n"
			printf "\t5 :ssd-mirror/KVM\n"
			printf "\t6 :torrents/\n"
			printf "\t7 :zroot/CACHE/torrents\n"
			printf "\nBACKUP\n"
			printf " -B\texport snapshot passed in \$1\n"
			printf "\nCREATION\n"
			printf "zfs create -o mountpoint=/mnt pool/dataset\n"
			printf "\nMISC\n"
			printf "zfs send pool/dataset@snapshot | zstd -T0 >| /tmp/backup.zst\n"
			printf "unzstd -c backup.zst | zfs receive pool/newdataset\n\n"
			printf "zfs set mountpoint=/newmount pool/dataset\n\n"
			printf "zfs snapshot -r zroot/ROOT/gentoo@<type>-<date>\n"
			printf "zfs rollback -r <pool/dataset@snapshot>\n"
			printf "zfs destroy <pool/dataset@snapshot>\n"
			printf "zfs list -t snapshot\n"
			printf "zfs list -r pool\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done
