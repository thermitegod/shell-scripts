# -*- coding: utf-8 -*-
# 1.1.0
# 2020-10-12

# Copyright (C) 2020 Brandon Zorn <brandonzorn@cock.li>
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


def confirm_run(text: str = None):
    if text is None:
        confirm = input('Confirm run [y/n]? ')
    else:
        confirm = input(text)

    if confirm in ('y', 'Y', 'yes', 'YES'):
        return True
    return False
