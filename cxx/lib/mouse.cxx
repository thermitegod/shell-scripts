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

#include <glibmm.h>

#include <ztd/ztd.hxx>

#include "lib/execute.hxx"
#include "lib/mouse.hxx"

#include "logger/logger.hxx"

void
mouse::set_position(const u32 x, const u32 y) noexcept
{
    auto result = execute::command_line_sync("swaymsg seat seat0 cursor set {} {}", x, y);
    if (result.exit_status != EXIT_SUCCESS)
    {
        logger::error("mouse::set_position() failed with code '{}'", result.exit_status);
        std::exit(result.exit_status);
    }
}

#if 0
std::array<u32, 2>
mouse::get_position() noexcept
{
    auto result = execute::command_line_sync("slurp -p");
    if (result.exit_status != EXIT_SUCCESS)
    {
        logger::error("mouse::get_position() failed with code '{}'", result.exit_status);
        std::exit(result.exit_status);
    }

    // Parse slurp position output
    // 1948,901 1x1
    const auto coords = ztd::partition(ztd::partition(result.standard_output, ' ')[0], ',');

    return {std::stoi(coords[0]), std::stoi(coords[2])};
}
#endif

void
mouse::left_click(const bool double_click) noexcept
{
    { // press
        auto result = execute::command_line_sync("swaymsg 'seat \"seat0\" cursor press button1'");
        if (result.exit_status != EXIT_SUCCESS)
        {
            logger::error("mouse::left_click() press failed with code '{}'", result.exit_status);
            std::exit(result.exit_status);
        }
    }

    { // release
        auto result = execute::command_line_sync("swaymsg 'seat \"seat0\" cursor release button1'");
        if (result.exit_status != EXIT_SUCCESS)
        {
            logger::error("mouse::left_click() release failed with code '{}'", result.exit_status);
            std::exit(result.exit_status);
        }
    }

    if (double_click)
    {
        left_click(false);
    }
}

void
mouse::right_click() noexcept
{
    { // press
        auto result = execute::command_line_sync("swaymsg 'seat \"seat0\" cursor press button3'");
        if (result.exit_status != EXIT_SUCCESS)
        {
            logger::error("mouse::right_click() press failed with code '{}'", result.exit_status);
            std::exit(result.exit_status);
        }
    }

    { // release
        auto result = execute::command_line_sync("swaymsg 'seat \"seat0\" cursor release button3'");
        if (result.exit_status != EXIT_SUCCESS)
        {
            logger::error("mouse::right_click() release failed with code '{}'", result.exit_status);
            std::exit(result.exit_status);
        }
    }
}
