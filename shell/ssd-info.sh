#!/usr/bin/env sh

# Copyright (C) ???? anon lainchan poster
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
# 1.3.0
# 2019-09-25


ssd_dev_1(){ SSD_DEVICE="/dev/disk/by-id/wwn-0x5002538da007852e" ; }
ssd_dev_2(){ SSD_DEVICE="/dev/disk/by-id/wwn-0x5002538d417e53d6" ; }
ssd_dev_3(){ SSD_DEVICE="/dev/disk/by-id/wwn-0x5002538d426ccd6a" ; }
#ssd_dev_3(){ SSD_DEVICE="" }

printf "SSD Devices\n"
ssd_dev_1;printf "1: ${SSD_DEVICE}\n"
ssd_dev_2;printf "2: ${SSD_DEVICE}\n"
ssd_dev_3;printf "3: ${SSD_DEVICE}\n"
read device

case "$device" in
	1) ssd_dev_1;;
	2) ssd_dev_2;;
	3) ssd_dev_3;;
	*) printf "INVALID\n";exit;;
esac

ON_TIME_TAG="Power_On_Hours"
WEAR_COUNT_TAG="Wear_Leveling_Count"
LBAS_WRITTEN_TAG="Total_LBAs_Written"
LBA_SIZE=512 # Value in bytes

BYTES_PER_MB=1048576
BYTES_PER_GB=1073741824
BYTES_PER_TB=1099511627776
BYTES_PER_PB=1125899906842624

# Get SMART attributes
SMART_INFO=$(sudo /usr/sbin/smartctl -A "$SSD_DEVICE")

# Extract required attributes
ON_TIME=$(echo "$SMART_INFO" | grep "$ON_TIME_TAG" | awk '{print $10}')
WEAR_COUNT=$(echo "$SMART_INFO" | grep "$WEAR_COUNT_TAG" | awk '{print $4}' | sed 's/^0*//')
LBAS_WRITTEN=$(echo "$SMART_INFO" | grep "$LBAS_WRITTEN_TAG" | awk '{print $10}')

# Convert LBAs -> bytes
BYTES_WRITTEN=$(echo "$LBAS_WRITTEN * $LBA_SIZE" | bc)
MB_WRITTEN=$(echo "scale=3; $BYTES_WRITTEN / $BYTES_PER_MB" | bc)
GB_WRITTEN=$(echo "scale=3; $BYTES_WRITTEN / $BYTES_PER_GB" | bc)
TB_WRITTEN=$(echo "scale=3; $BYTES_WRITTEN / $BYTES_PER_TB" | bc)
PB_WRITTEN=$(echo "scale=3; $BYTES_WRITTEN / $BYTES_PER_PB" | bc)

# Output results...
echo "-------------------------------"
echo " SSD Status:   $SSD_DEVICE"
echo "-------------------------------"
echo " On time:      $(echo $ON_TIME | sed ':a;s/\B[0-9]\{3\}\>/,&/;ta') hr"
echo "-------------------------------"
echo " Data written:"
echo "           MB: $(echo $MB_WRITTEN | sed ':a;s/\B[0-9]\{3\}\>/,&/;ta')"
echo "           GB: $(echo $GB_WRITTEN | sed ':a;s/\B[0-9]\{3\}\>/,&/;ta')"
echo "           TB: $(echo $TB_WRITTEN | sed ':a;s/\B[0-9]\{3\}\>/,&/;ta')"
echo "           PB: $(echo $PB_WRITTEN | sed ':a;s/\B[0-9]\{3\}\>/,&/;ta')"
echo "-------------------------------"
echo " Mean write rate:"
echo "        MB/hr: $(echo "scale=3; $MB_WRITTEN / $ON_TIME" | bc | sed ':a;s/\B[0-9]\{3\}\>/,&/;ta')"
echo "-------------------------------"
echo " Drive health: ${WEAR_COUNT} %"
echo "-------------------------------"
