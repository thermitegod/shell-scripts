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

#include "lib/hash.hxx"

/**
 * @brief Shell Quote
 *
 * - quote string so that is will work with Glib::spawn_command_line_sync
 *
 * @param[in] str The string to be quoted
 *
 * @return a quoted string, if string is empty returns empty quotes
 */
[[nodiscard]] const std::string
shell_quote(const std::string_view str) noexcept
{
    if (str.empty())
    {
        return "\"\"";
    }
    return std::format("\"{}\"", ztd::replace(str, "\"", "\\\""));
}

bool
hash::compare_files(const std::filesystem::path& a, const std::filesystem::path& b) noexcept
{
    // Glib::find_program_in_path("xxhsum");

    const std::string command_a = std::format("xxhsum {}", shell_quote(a.c_str()));
    std::string stdout_a;
    Glib::spawn_command_line_sync(command_a, &stdout_a);

    const std::string command_b = std::format("xxhsum {}", shell_quote(b.c_str()));
    std::string stdout_b;
    Glib::spawn_command_line_sync(command_b, &stdout_b);

    const std::string a_hash = ztd::partition(stdout_a, " ")[0];
    const std::string b_hash = ztd::partition(stdout_b, " ")[0];

    // logger::info("A : {} | {}", a_hash, a);
    // logger::info("B : {} | {}", b_hash, b);
    // logger::info("================");

    return a_hash == b_hash;
}
