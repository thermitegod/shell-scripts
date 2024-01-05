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

#pragma once

#include <string_view>

namespace colors
{
// reset
constexpr std::string_view nc = "\033[0m";

// regular
constexpr std::string_view bla = "\033[0;30m";
constexpr std::string_view red = "\033[0;31m";
constexpr std::string_view gre = "\033[0;32m";
constexpr std::string_view yel = "\033[0;33m";
constexpr std::string_view blu = "\033[0;34m";
constexpr std::string_view pur = "\033[0;35m";
constexpr std::string_view cya = "\033[0;36m";
constexpr std::string_view whi = "\033[0;37m";

// bold
constexpr std::string_view bbla = "\033[1;30m";
constexpr std::string_view bred = "\033[1;31m";
constexpr std::string_view bgre = "\033[1;32m";
constexpr std::string_view byel = "\033[1;33m";
constexpr std::string_view bblu = "\033[1;34m";
constexpr std::string_view bpur = "\033[1;35m";
constexpr std::string_view bcya = "\033[1;36m";
constexpr std::string_view bwhi = "\033[1;37m";

// underline
constexpr std::string_view ubla = "\033[4;30m";
constexpr std::string_view ured = "\033[4;31m";
constexpr std::string_view ugre = "\033[4;32m";
constexpr std::string_view uyel = "\033[4;33m";
constexpr std::string_view ublu = "\033[4;34m";
constexpr std::string_view upur = "\033[4;35m";
constexpr std::string_view ucya = "\033[4;36m";
constexpr std::string_view uwhi = "\033[4;37m";

// high intensity
constexpr std::string_view ibla = "\033[0;90m";
constexpr std::string_view ired = "\033[0;91m";
constexpr std::string_view igre = "\033[0;92m";
constexpr std::string_view iyel = "\033[0;93m";
constexpr std::string_view iblu = "\033[0;94m";
constexpr std::string_view ipur = "\033[0;95m";
constexpr std::string_view icya = "\033[0;96m";
constexpr std::string_view iwhi = "\033[0;97m";

// bold high intensity
constexpr std::string_view bibla = "\033[1;90m";
constexpr std::string_view bired = "\033[1;91m";
constexpr std::string_view bigre = "\033[1;92m";
constexpr std::string_view biyel = "\033[1;93m";
constexpr std::string_view biblu = "\033[1;94m";
constexpr std::string_view bipur = "\033[1;95m";
constexpr std::string_view bicya = "\033[1;96m";
constexpr std::string_view biwhi = "\033[1;97m";

// background
constexpr std::string_view on_bla = "\033[40m";
constexpr std::string_view on_red = "\033[41m";
constexpr std::string_view on_gre = "\033[42m";
constexpr std::string_view on_yel = "\033[43m";
constexpr std::string_view on_blu = "\033[44m";
constexpr std::string_view on_pur = "\033[45m";
constexpr std::string_view on_cya = "\033[46m";
constexpr std::string_view on_whi = "\033[47m";

// high intensity backgrounds
constexpr std::string_view on_ibla = "\033[0;100m";
constexpr std::string_view on_ired = "\033[0;101m";
constexpr std::string_view on_igre = "\033[0;102m";
constexpr std::string_view on_iyel = "\033[0;103m";
constexpr std::string_view on_iblu = "\033[0;104m";
constexpr std::string_view on_ipur = "\033[0;105m";
constexpr std::string_view on_icya = "\033[0;106m";
constexpr std::string_view on_iwhi = "\033[0;107m";
} // namespace colors
