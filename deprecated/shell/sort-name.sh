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
# 2019-01-17


#keeping it simple, since v2

#TODO
#improve multi list

die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }

main()
{
	while IFS=' ' read -r name override;do
		name_sort
	done < "${list_sort}"
}

name_sort()
{
	if [ -n "$(echo "${name}"|grep '\#')" ];then return;fi
	arc="$(echo "${name}" | sed -e "s/\-/\*/g")"
	if [ -z "${override}" ];then dir="${name}/.";else dir="${override}/.";fi

	if [ "${debug}" -ge "2" ];then printf "${BLU}\$name${NC}: %s\n" "${name}";fi
	if [ "${debug}" -ge "3" ];then printf "\t${CYA}\$arc${NC}: %s\n" "${arc}";fi
	if [ "${debug}" -ge "3" ];then printf "\t${CYA}\$dir${NC}: %s\n" "${dir}";fi

	case "${job_run}" in
		dir_check)
			find . -maxdepth 1 -type f -iname "*${arc}*" -exec mkdir -p -- "${dest}/${dir}" \; -quit
			;;
		sort_main)
			find . -maxdepth 1 -type f -iname "*${arc}*" -exec mv -n -- "{}" "${dest}/${dir}" \;
			;;
		sort_local)
			find . -maxdepth 1 -type f -iname "*${arc}*" -exec mkdir -p -- "${PWD}/${dir}" \; -exec mv -i -- "{}" "${PWD}/${dir}" \;
			;;
	esac
}

B="$(ls -1A|wc -l)"
debug="0"
total="0"

. "$(dirname "$0")/colors.sh"

print_sorted_total="1"

list_final="${XDG_DATA_HOME}/shell/sort-name-final"
list_type="${XDG_DATA_HOME}/shell/sort-name-type"
dest_final="$(head -n1 "${list_final}"|sed -e "s/#//g")"
dest_type=$(head -n1 "${list_type}"|sed -e "s/#//g")

#default
list_sort="${list_type}"
dest="${dest_type}"

while getopts "ETefthd:" OPT;do
	case "$OPT" in
		f) list_sort="${list_final}";dest="${dest_final}";;
		t) list_sort="${list_type}";dest="${dest_type}";;
		d)
			case "${OPTARG}" in
				1) debug="1";;
				2) debug="2";;
				3|*) debug="3";;
			esac;;
		T) dest="/tmp/test";;
		E) $EDITOR "${list_final}";exit;;
		e) $EDITOR "${list_type}";exit;;
		h)
			printf " -d #\tDebug output, prints vars, levels [1,3]\n"
			printf " -h\tPrint this help\n"
			printf " -T\tUse test dir \"/tmp/test\"\n"
			printf "\nEDIT\n"
			printf " -e\tedit %s\n" "${list_type}"
			printf " -E\tedit %s\n" "${list_final}"
			printf "\nLIST\n"
			printf " -f\trun final sort\n"
			printf " -t\trun type sort\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done

if ! [ -f "${list_sort}" ];then
	printf "missing: %s\nformat, line 1 must be default save path:\n/path/to/save\nto-sort\nto-sort override\n" "${list_sort}"
	die
fi

if [ "${debug}" -ge "1" ];then printf "\n*** Debug printouts enabled ***\n\n";fi
printf "Prerun info\n"
printf "MODE\t\t: %s\n" "$(basename "${list_sort}")"
printf "Running from\t: %s\n" "${PWD}"
printf "Dest is\t\t: %s\n\n" "${dest}"
printf "Make sure everything has been processed correctly\n"
printf "\nRunning script is: '%s'\n" "${0}"
read -r -p "Confirm run [yn]? " confirm
if echo "${confirm}"|grep -iq "^y" ;then
	#all target dirs should exits before running
	#otherwise you are going to have a bad time
	if [ "${debug}" -ge "1" ];then printf "${YEL}Debug${NC}: running dir_check\n";fi
	job_run="dir_check"
	main
	#move maches to dest
	if [ "${debug}" -ge "1" ];then printf "${YEL}Debug${NC}: running sort_main\n";fi
	job_run="sort_main"
	main
	#deal w/ name collisions in dest by sorting into $pwd, to be delt w/ manualy
	if [ "${debug}" -ge "1" ];then printf "${YEL}Debug${NC}: running sort_local\n";fi
	job_run="sort_local"
	main
else
	printf "Did not confirm, Exiting.\n"
	die
fi

if [ "${print_sorted_total}" = "1" ];then
	A="$(ls -1A|wc -l)"
	T="$((B-A))"
	if ! [ "${total}" = "0" ];then
		printf "\n${YEL}BEFORE${NC}\t%s\n" "${B}"
		printf "${YEL}AFTER${NC}\t%s\n" "${A}"
		printf "${YEL}SORTED${NC}\t%s\n" "${T}"
	fi
fi
