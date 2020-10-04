#!/usr/bin/env sh
#1.1.0
#2019-12-01

# Copyright (C) 2019 Brandon Zorn <brandonzorn@cock.li>
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

#not using sys-kernel/linux-firmware[initramfs]
#since i only need an img with fam17h

#based on: https://wiki.gentoo.org/wiki/AMD_microcode

die(){ /bin/echo -e "\033[0;31m$*\033[m";exit 1; }

if [ "$(id -u)" -ne 0 ];then die "Requires root";fi

finish(){ if [ -d "${tmpdir}" ];then rm --preserve-root -r "${tmpdir}";fi; }
trap 'exit 1' INT HUP QUIT TERM USR1
trap finish EXIT
tmpdir="$(mktemp -d)"

tmpdir_deep="kernel/x86/microcode"
amd_micro="/lib/firmware/amd-ucode/microcode_amd_fam17h.bin"
amd_micro_boot="/boot/amd-uc.img"

if [ -f "${amd_micro_boot}" ];then
	rm "${amd_micro_boot}"
fi

mkdir -p "${tmpdir}/${tmpdir_deep}"
cd "${tmpdir}" || die
#cat "${amd_micro}" >| "${tmpdir_deep}/AuthenticAMD.bin" #only needed if using multiple *.bin files
cp "${amd_micro}" "${tmpdir_deep}/AuthenticAMD.bin" #since only one *.bin file is used just use cp
echo "${tmpdir_deep}/AuthenticAMD.bin" | bsdcpio -o -H newc -R 0:0 >| "${amd_micro_boot}"

