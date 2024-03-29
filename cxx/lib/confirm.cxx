/**
 * Copyright (C) 2024 Brandon Zorn <brandonzorn@cock.li>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

#include <string>
#include <string_view>

#include <iostream>

#include <unistd.h>

#include <ztd/ztd.hxx>

bool
confirm_run(std::string_view prompt) noexcept
{
    std::string val;
    std::cout << prompt << std::endl;
    if (std::getline(std::cin, val))
    {
        if (ztd::lower(val) == "y" || ztd::lower(val) == "yes" || val == "1")
        {
            return true;
        }
        return false;
    }
    return false;
}
