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
# 8.1.0
# 2019-02-13


#misc
#lxc will not mount on symlinks, but can mount through them

#TODO
#condense main function
#portability

set_dirs()
{
	#not in container
	storage="/mnt/torrents"
	config="${storage}/.config/${cname}"
	session="${config}/session"
	watch="${config}/watch"
	save="${storage}/${cname}"
	if [ -n "${save_override}" ];then save="${save_override}";fi
	#in container
	case "${ctype}" in
		rutorrent)
			case "${distro}" in
				alpine)
					var="/usr/share/webapps/rutorrent/share"
					;;
				gentoo)
					var="/var/www/localhost/htdocs/rutorrent/share"
					;;
			esac
			rushare="${config}/rutorrent/share"
			setbase="/home/${user}"
			inside_data="${setbase}/rtorrent/data"
			inside_watch="${setbase}/rtorrent/watch"
			inside_session="${setbase}/rtorrent/session"
			;;
		transmission)
			setbase="/var/lib/transmission"
			inside_data="${setbase}/downloads"
			inside_session="${setbase}/config"
			;;
	esac

	if [ "${get_dirs}" = "1" ];then return;fi

	if ! [ -e "${config}" ];then mkdir -pv "${config}";fi
	if ! [ -e "${save}" ];then mkdir -pv "${save}";fi
	if ! [ -e "${session}" ];then mkdir -pv "${session}";fi
	if ! [ -e "${watch}" ] && [ "${ctype}" = "rutorrent" ];then mkdir -pv "${watch}";fi
	if ! [ -e "${rushare}" ] && [ "${ctype}" = "rutorrent" ];then mkdir -pv "${rushare}";fi

	lxc config device add "${fullname}" storage disk source="${save}" path="${inside_data}"
	lxc config device add "${fullname}" session disk source="${session}" path="${inside_session}"
	if [ "${ctype}" = "rutorrent" ];then
		lxc config device add "${fullname}" watch disk source="${watch}" path="${inside_watch}"
		lxc config device add "${fullname}" ru disk source="${rushare}" path="${var}"
	fi
}

get_state(){ if [ "$(lxc info "${1}"|grep Running)" ];then is_running="1";fi; }

main_container()
{
	if [ "${ctype}" = "version" ];then
		if ! [ "${distro}" = "${config_version}" ];then
			printf "Config file format has changed\n"
			printf "update existing config file to new version\n\n"
			printf "Current version: %s\n" "${distro}"
			printf "New version: %s\n" "${config_version}"
			exit 1
		fi
	fi

	#TODO: need to find a better way to do this
	#order matters here
	if [ -n "$(echo "${ctype}"|grep '\#')" ];then return;fi #skip comments
	if [ -n "$(echo "${ctype}"|grep stop)" ];then exit;fi #exit when 'stop' is read
	if [ -z "${cname}" ];then return;fi #skip blank lines

	case "${distro}" in #make less shit
		alpine) a="1";;
		gentoo) a="1";;
		*) printf "skipping non supported distro: %s\n" "${distro}";return;;
	esac

	template="base-${distro}-${ctype}"
	fullname="${ctype}-${cname}"

	if [ "${on_old}" = "1" ];then
		fullname="${old_prefix}-${fullname}"
	fi

	if [ "${catch_single}" = "1" ];then
		if ! [ "${catch}" = "${fullname}" ];then return;fi
	fi

	if [ "${limit_ctype}" = "1" ];then
		if ! [ "${limit_to}" = "${ctype}" ];then return;fi
	fi

	if [ "${limit_level}" = "1" ];then
		if ! [ "${level_limit}" = "${level}" ];then return;fi
	fi

	case "${act}" in
		stop)
			get_state "${fullname}"
			if [ "${is_running}" = "0" ];then return;fi
			printf "Stopping container: %s\n" "${fullname}";lxc stop "${fullname}" &
			;;
		start)
			if [ "${autostart}" = "0" ];then return;fi
			get_state "${fullname}"
			if [ "${is_running}" = "1" ];then return;fi
			printf "Starting container: %s\n" "${fullname}";sleep .1;lxc start "${fullname}" &
			;;
		delete)
			get_state "${fullname}"
			if [ "${is_running}" = "1" ];then printf "Must stop before deleting: %s\n" "${fullname}";return;fi
			printf "Deleteing container: %s\n" "${fullname}";lxc delete "${fullname}" &
			;;
		restart)
			get_state "${fullname}"
			if [ "${is_running}" = "0" ];then return;fi
			printf "Restarting container: %s\n" "${fullname}";lxc restart "${fullname}" &
			;;
		forcestop)
			get_state "${fullname}"
			if [ "${is_running}" = "0" ];then return;fi
			printf "Force stopping container: %s\n" "${fullname}";lxc stop --force "${fullname}" &
			;;
		rtorrent_clean_lock)
			get_state "${fullname}"
			if [ "${is_running}" = "1" ];then printf "Not cleaning lock on running: %s\n" "${fullname}";return;fi
			get_dirs="1"
			set_dirs
			lock="${session}/rtorrent.lock"
			if [ -f "${lock}" ];then rm -v "${lock}";fi
			get_dirs="0"
			;;
		rtorrent_clean_torrent)
			#printf "Running cleanup for: "${fullname}"\n"
			set_dirs
			if [ "${htpasswd}" = "1" ];then
				torrent_files_path="${rushare}/users/${user}/torrents"
			else
				torrent_files_path="${rushare}/torrents"
			fi
			if ! [ "$(ls -1A "${torrent_files_path}"|wc -l)" = "0" ];then
				rm "${torrent_files_path}"/*.torrent
			fi
			;;
		restart_service)
			get_state "${fullname}"
			if [ "${is_running}" = "0" ];then return;fi
			printf "\nRestarting %s on: %s\n\n"  "${service}" "${fullname}"
			lxc exec "${fullname}" rc-service "${service}" restart >/dev/null 2>&1 &
			;;
		update)
			get_state "${fullname}"
			if [ "${is_running}" = "1" ];then
				printf "Not updating running container: %s\n" "${fullname}"
				return
			fi

			get_state "${template}"
			if [ "${is_running}" = "1" ];then
				printf "Stopping running template: %s\n" "${template}"
				lxc stop "${template}"
				printf "\n\n"
			fi

			printf "Update running for: %s\n" "${fullname}"

			if [ "$(echo "${lxclist}"|grep "${fullname}")" ];then
				if [ "${update_keep_old}" = "1" ];then
					printf "Renaming %s to %s-%s\n" "${fullname}" "${old_prefix}" "${fullname}"
					lxc rename "${fullname}" "${old_prefix}-${fullname}"
				elif [ "${update_keep_old}" = "0" ];then
					printf "Deleting %s\n" "${fullname}"
					lxc delete "${fullname}"
				fi
			fi

			printf "Copying %s to %s\n" "${template}" "${fullname}"
			lxc copy "${template}" "${fullname}"

			if [ "${distro}" = "gentoo" ];then
				#removes unneeded access to filesystem on gentoo containers
				lxc config device remove "${fullname}" distfiles
				lxc config device remove "${fullname}" packages
				lxc config device remove "${fullname}" repos
			fi

			if ! [ "${lim_cpu}" = "0" ];then lxc config set "${fullname}" limits.cpu "${lim_cpu}";fi
			if ! [ "${lim_cpu_allow}" = "0" ];then lxc config set "${fullname}" limits.cpu.allowance "${lim_cpu_allow}";fi
			if ! [ "${lim_mem}" = "0" ];then lxc config set "${fullname}" limits.memory "${lim_mem}";fi

			#clean rtorrent lock files
			if [ "${ctype}" = "rutorrent" ];then
				"${0}" -c -O "${fullname}"
			fi

			printf "Seting StaticIP to: %s\n" "${ip4}"
			net_tmp=$(mktemp)
			case "${distro}" in
				alpine)
					net="${fullname}/etc/network/interfaces"
					printf "auto eth0\niface eth0 inet static\n\taddress %s\n\tnetmask %s\n\tgateway %s\n" "${ip4}" "${ip4_netmask}" "${ip4_gateway}">|"${net_tmp}"
					;;
				gentoo)
					net="${fullname}/etc/conf.d/net"
					printf "rc_keyword=\"-stop\"\nconfig_eth0=\"%s netmask %s brd %s\"\nroutes_eth0=\"default via %s\"\n" "${ip4}" "${ip4_netmask}" "${ip4_brd}" "${ip4_gateway}">|"${net_tmp}"
					;;
			esac
			lxc file push "${net_tmp}" "${net}"
			if [ -f "${net_tmp}" ];then rm "${net_tmp}";fi

			set_dirs
			printf "\n"
			;;
		print)
			get_state "${fullname}"
			printf "Container Name\t: %s\n" "${fullname}"
			printf "Name\t\t: %s\n" "${cname}"
			printf "Template\t: %s\n" "${ctype}"
			printf "Distro\t\t: %s\n" "${distro}"
			if [ "${ctype}" = "transmission" ];then ip4="${ip4}:${transmission_port}";fi
			printf "IPV4\t\t: %s\n" "${ip4}"
			if [ "${is_running}" = "1" ];then state="on";else state="off";fi
			printf "On/Off\t\t: %s\n" "${state}"
			printf "Autostart\t: %s\n" "${autostart}"
			if [ "${verbose}" = "1" ];then
				printf "User\t\t: %s\n" "${user}"
				printf "htpasswd\t: %s\n" "${htpasswd}"
				printf "Level\t\t: %s\n" "${level}"
				printf "Limit CPU\t: %s\n" "${lim_cpu}"
				printf "Limit CPU ALLOW\t: %s\n" "${lim_cpu_allow}"
				printf "Limit MEM\t: %s\n" "${lim_mem}"
				set_dirs
				printf "session\t\t: %s\n" "${session}"
				if [ "${ctype}" = "rutorrent" ];then
					printf "rushare\t\t: %s\n" "${rushare}"
					printf "watch\t\t: %s\n" "${watch}"
				fi
				printf "save\t\t: %s\n" "${save}"
				if [ -n "${save_override}" ];then printf "save override\t: active\n";fi
			fi
			printf "\n"
			;;
	esac
}

on_old="0"
verbose="0"
get_dirs="0"
is_running="0"
catch_single="0"

limit_to="z"
limit_ctype="0"
limit_level="0"

update_keep_old="1"

transmission_port="9091"

ip4_brd="192.168.0.255"
ip4_gateway="192.168.0.1"
ip4_netmask="255.255.255.0"

old_prefix="old"
lxclist="$(lxc list)"

config_version="2"
config_containers="${XDG_DATA_HOME}/shell/lxd-admin"

if [ -z "${1}" ];then "${0}" -h;exit;fi
while getopts "O:l:TRCPZUHEScdrsuzpheo" OPT;do
	case "${OPT}" in
		O) catch_single="1";catch=${OPTARG};;
		T) limit_ctype="1";limit_to="transmission";;
		R) limit_ctype="1";limit_to="rutorrent";;
		o) on_old="1";;
		c) act="rtorrent_clean_lock";limit_to="rutorrent";;
		C) act="rtorrent_clean_torrent";limit_to="rutorrent";get_dirs="1";;
		d) act="delete";;
		r) act="restart";;
		s) act="start";;
		u) act="update";;
		U) act="update";update_keep_old="0";;
		z) act="stop";;
		Z) act="forcestop";;
		p) act="print";;
		P) act="print";get_dirs="1";verbose="1";;
		S) act="restart_service";service="${OPTARG}";;
		l) level_limit="${OPTARG}";limit_level="1";;
		e) ${EDITOR} "${config_containers}";exit;;
		E) cat "${config_containers}";exit;;
		h)
			printf "CONTAINER, only use to limit actions to specified\n"
			printf " -R\tOnly run on rutorrent\n"
			printf " -T\tOnly run on transmission, note: port is :%s\n" "${transmission_port}"
			printf " -O\tOnly operate in the supplied container, requires full container name\n"
			printf " -o\tOnly operate on containers with '%s' prefix\n" "${old_prefix}"
			printf " -l #\tOnly operate on cantainers in this level\n"
			printf "\nCONTAINER SERVICES\n"
			printf " -S\trestart service passed as arg\n"
			printf "\nCONTAINER GENERAL\n"
			printf " -d\tDelete containers\n"
			printf " -h\tPrint this help\n"
			printf " -H\tprint file setup guide: %s\n" "${config_containers}"
			printf " -r\tRestart containers\n"
			printf " -s\tStart containers\n"
			printf " -u\tUpdate, rename existing with '%s' prefix\n" "${old_prefix}"
			printf " -U\tUpdate, delete existing instead of renaming\n"
			printf " -z\tStop containers\n"
			printf " -Z\tForce stop containers\n"
			printf "\nSPECIFIC, no other flags req\n"
			printf " -c\trtorrent lockfile cleanup\n"
			printf " -C\trutorrent cleanup only, remove *.torrent files in \$config/rutorrent/share/torrents/\n"
			printf "\nOTHER\n"
			printf " -e\tedit %s\n" "${config_containers}"
			printf " -E\tcat %s\n" "${config_containers}"
			printf " -P\tPrint all container vars\n"
			printf " -p\tPrint limited container vars\n"
			exit;;
		H)
			printf "==SUBJECT TO CHANGE==\n\n"
			printf "Config version: ${config_version}\n\n"
			printf "All containers are declared in '%s' using the following space delimited format\n\n" "${config_containers}"

			printf "Valid values are\n"
			printf "================\n"
			printf "container type: rutorrent, transmission, stop\n"
			printf "distro: gentoo, alpine\n"
			printf "user: user used in container\n"
			printf "autostart: 0, 1\n"
			printf "htpasswd: 0, 1\n"
			printf "level: any int\n"
			printf "ipv4: a local ip4v address\n"
			printf "limit cpu: any int\n"
			printf "limit cpu allowance: any percent\n"
			printf "limit mem: any int with a unit\n"
			printf "container name: any string\n"
			printf "save location override, optional: a path\n\n"

			printf "Example\n"
			printf "version ${config_version}\n"
			printf "rutorrent gentoo brandon 1 1 1 192.168.0.161 6 10%% 8192MB anime /mnt/anime/anime-working\n\n"

			printf "Config file parsing\n"
			printf "supports comments, no inline comments\n"
			printf "Script will stop if 'container type' is set to 'stop'\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done
#shift $((OPTIND - 1))

if ! [ -f "${config_containers}" ];then "${0}" -H;exit 1;fi

while IFS=' ' read -r ctype distro user autostart htpasswd level ip4 lim_cpu lim_cpu_allow lim_mem cname save_override;do
	main_container
done < "${config_containers}"

