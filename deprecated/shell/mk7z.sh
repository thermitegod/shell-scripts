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
# 3.8.0
# 2020-05-01


#notes
#resources: https://sevenzip.osdn.jp/chm/cmdline/switches/method.htm
#m0=lzma2 is fast mode but produces samller archives, needs more testing
#-m prefixes all options or -m0=lzma:a1:d25 for sub options

#NOTICE: The compression profiles being used will probably use =LOTS= of ram

die(){ /bin/echo -e "$*";exit 1; }

die_failed(){ die "${RED}Compression failed for${NC}: ${f%%}"; }

test_file_list(){ if [ -f "${f%%}.7z" ];then file_list="${file_list}${delim}${f%%}.7z";fi; }

extra_info()
{
	if [ "${extra}" = "1" ];then
		printf "\n"
		printf "${YEL}Profile\t: %s${NC}\n" "${comp_type}"
		printf "${YEL}File\t: %s${NC}\n" "${f%%}"
	fi
}

compress()
{
	case "${comp_type}" in
		single)
			extra_info
			nice -19 \
				7zr a -t7z -m0=lzma2 -md=1024m -mmf=bt4 -mmt=off -ms=off -myx=9 -mx=9 -mfb=276 \
				-ms=on -mhc=on -mtm=off -mtc=off -mta=off "${f%%}.7z" "${f%%}" || die_failed
			test_file_list
			;;
		multi)
			extra_info
			nice -19 \
				7zr a -t7z -m0=lzma2 -md=1024m -mmf=bt4 -mmt=on -mmtf=on -myx=9 -mx=9 -mfb=276 \
				-mhc=on -ms=on -mtm=off -mtc=off -mta=off "${f%%}.7z" "${f%%}" || die_failed
			test_file_list
			;;
		test)
			if [ "${f##*.}" = "7z" ] || [ "${f##*.}" = "zip" ];then
				#limits line length to 80, does not like line wraping
				printf "${YEL}TEST${NC}\t%s\n" "$(echo "${f%%}"|cut -c 1-80)"
				printf "\033[A"
				if [ -n "$(nice -19 7z t "${f%%}"|grep Ok)" ];then
					printf "${GRE}PASSED${NC}\t%s\n" "${f%%}"
					P=$((P+1))
				else
					printf "%s\n" "${f}">>failed.txt
					printf "${RED}FAILED${NC}\t%s\n" "${f%%}"
					F=$((F+1))

					if [ "${move_failed_file}" = "1" ];then
						failed_dir="$(dirname "${f%%}")/mk7z-failed"
						if ! [ -d "${failed_dir}" ];then mkdir "${failed_dir}";fi
						mv "${f%%}" "${failed_dir}"
					fi
				fi
			fi
			;;
	esac

	if [ "$?" -eq 0 ] && ! [ "${comp_type}" = "test" ] && [ "${orig_rm}" = "1" ] && [ -f "${f%%}.7z" ];then
		if [ -n "$(${0} -t "${f%%}.7z"|grep FAILED)" ];then
			printf "${RED}FAILED${NC} test for: %s.7z\n${YEL}Not removing original${NC}: %s\n" "${f%%}" "${f%%}"
		else
			rm -r "${f%%}"
		fi
	fi
}

P="0"
F="0"

extra="0"
total="0"
orig_rm="0"
comp_dir="0"
comp_file="0"

move_failed_file="1"

test_post="1"
file_list=""
comp_type="multi"
test_post_fancy="1"

delim=",ßßß,"

. "$(dirname "$0")/colors.sh"

while getopts "SMTROPEetdfhxz" OPT;do
	case "$OPT" in
		S) comp_type="single";;
		M) comp_type="multi";;
		t) comp_type="test";test_post="0";printf "${YEL}RUNNING TESTS${NC}\n";;
		T) comp_type="test";test_post="0";test_post_fancy="0";;
		P) test_post="0";;
		d) comp_dir="1";;
		f) comp_file="1";;
		R) orig_rm="1";test_post="0";;
		x) comp_file="1";orig_rm="1";;
		z) comp_dir="1";orig_rm="1";;
		e) extra="1";;
		E) move_failed_file="0";;
		h)
			printf " default will compress file passed in \$1\n"
			printf "\nGENERAL\n"
			printf " -e\tprint extra info\n"
			printf "\nPROFILES\n"
			printf " -S\tSingle threaded, useful when hitting oom with multi\n"
			printf " -M\tMultithreaded\n"
			printf "\nOTHER\n"
			printf " -E\tDisable moving files that fail tests to subdirectory\n"
			printf " -d\tcompress all directories\n"
			printf " -f\tcompress all files\n"
			printf " -h\tprint this help\n"
			printf " -P\tDisable post compression test\n"
			printf " -R\tdelete after compressed, will test before deleting, disables post testing, works in all modes but test\n"
			printf " -t\tTest file[s] passed in \$1\n"
			printf " -T\tTest file[s] passed in \$1 disable total output\n"
			printf " -x\tcompress all files, delete original after compressed\n"
			printf " -z\tcompress all directories, delete original after compressed\n"
			exit;;
		*) printf "Showing help\n\n";"${0}" -h;;
	esac
done
shift $((OPTIND - 1))

if [ -n "${1}" ];then
	while true;do
		f="${1%%}"
		if [ -e "${f}" ];then
			compress
		else
			printf "\n${RED}Input does not exist${NC}: %s\n\n" "${1}"
		fi
		if [ -n "${2}" ];then shift;else break;fi
	done
elif [ "${comp_dir}" = "1" ] || [ "${comp_file}" = "1" ];then
	for f in *; do
		if [ "${comp_dir}" = "1" ] && [ -d "${f%%}" ];then compress;fi
		if [ "${comp_file}" = "1" ] && [ -f "${f%%}" ];then compress;fi
	done
else
	printf "\n${RED}No input files${NC}\n\n";exit
fi

if [ "${test_post}" = "1" ] && [ "${orig_rm}" = "0" ];then
	IFS="${delim}"
	for f in ${file_list}; do
		if [ -f "${f}" ];then
			comp_type="test"
			compress
		fi
	done
	unset IFS
fi

if [ "${comp_type}" = "test" ] && [ "${test_post_fancy}" = "1" ];then
	T="$((P+F))"
	if ! [ "${total}" = "0" ];then
		printf "\n${YEL}TOTAL${NC} \t%s\n" "${T}"
		if ! [ "${P}" = "0" ];then printf "${GRE}PASSED${NC}\t%s\n" "${P}";fi
		if ! [ "${F}" = "0" ];then printf "${RED}FAILED${NC}\t%s\n" "${F}";fi
	fi
fi
