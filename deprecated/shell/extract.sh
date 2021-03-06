#!/usr/bin/env sh
#1.7.1
#2020-05-12

#original unknown
#modified by, Brandon Zorn <brandonzorn@cock.li>

while true;do
	if [ -f "${1}" ];then
		case "${1}" in
			*.tgz|*.tbz2) tar xvf "${1}";break;;
			*.txz) tar xvJf "${1}";break;;
			*.tar.bz2) tar xvjf "${1}";break;;
			*.tar.gz) tar xvzf "${1}";break;;
			*.tar.xz) tar xvJf "${1}";break;;
			*.tar.zst) zstd -dc --long=31 "${1}"|tar xvf -;break;;
			*.tar.lz4) lz4 -dc "${1}"|tar xvf -;break;;
			*.tar.lzma) tarlzma xvf "${1}";break;;
			*.tar.lrz) lrzuntar "${1}";break;;
			*.rar|*.RAR) unrar "${1}";break;;
			*.gz) gunzip -k "${1}";break;;
			*.xz) unxz -k "${1}";break;;
			*.bz2) bzip2 -dk "${1}";break;;
			*.zst) unzstd -d --long=31 "${1}";break;;
			*.tar) tar xvf "${1}";break;;
			*.zip) unzip "${1}";break;;
			*7z|*.iso|*.ISO) 7z x "${1}";break;;
			*.cbz|*.cbr) 7z x "${1}" -o"${1}";break;;
			*) printf "cannot extract: %s\n" "${1}";break;;
		esac
	else
		printf "not a valid file: %s\n" "${1}"
	fi
	if [ -n "${2}" ];then shift;else break;fi
done
