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

#include <format>

#include <filesystem>

#include <glibmm.h>

#include <ztd/ztd.hxx>

#include "logger/logger.hxx"

#include "lib/execute.hxx"
#include "lib/hash.hxx"

bool
hash::compare_files(const std::filesystem::path& a, const std::filesystem::path& b) noexcept
{
    // Glib::find_program_in_path("xxhsum");

    auto result_a = execute::command_line_sync("xxhsum {}", execute::quote(a.c_str()));
    auto result_b = execute::command_line_sync("xxhsum {}", execute::quote(b.c_str()));

    const std::string a_hash = ztd::partition(result_a.standard_output, " ")[0];
    const std::string b_hash = ztd::partition(result_b.standard_output, " ")[0];

    // logger::info("A : {} | {}", a_hash, a);
    // logger::info("B : {} | {}", b_hash, b);
    // logger::info("================");

    return a_hash == b_hash;
}
