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

#include "lib/mouse.hxx"

#include "logger/logger.hxx"

void
mouse::set_position(const u32 x, const u32 y) noexcept
{
    const auto command = std::format("swaymsg seat seat0 cursor set {} {}", x, y);

    std::int32_t exit_status = EXIT_SUCCESS;
    Glib::spawn_command_line_sync(command, nullptr, nullptr, &exit_status);
    if (exit_status != EXIT_SUCCESS)
    {
        logger::error("mouse::set_position() failed with code '{}'", exit_status);
        std::exit(exit_status);
    }
}

#if 0
std::array<u32, 2>
mouse::get_position() noexcept
{
    std::string standard_output;
    std::int32_t exit_status = EXIT_SUCCESS;
    Glib::spawn_command_line_sync("slurp -p", &standard_output, nullptr, &exit_status);
    if (exit_status != EXIT_SUCCESS)
    {
        logger::error("mouse::get_position() failed with code '{}'", exit_status);
        std::exit(exit_status);
    }

    // Parse slurp position output
    // 1948,901 1x1
    const auto coords = ztd::partition(ztd::partition(standard_output, ' ')[0], ',');

    return {std::stoi(coords[0]), std::stoi(coords[2])};
}
#endif

void
mouse::left_click(const bool double_click) noexcept
{
    // swaymsg 'seat "seat0" cursor press button1' && swaymsg 'seat "seat0" cursor release button1'

    const auto press = "swaymsg 'seat \"seat0\" cursor press button1'";
    const auto release = "swaymsg 'seat \"seat0\" cursor release button1'";

    std::int32_t exit_status = EXIT_SUCCESS;
    Glib::spawn_command_line_sync(press, nullptr, nullptr, &exit_status);
    if (exit_status != EXIT_SUCCESS)
    {
        logger::error("mouse::left_click() press failed with code '{}'", exit_status);
        std::exit(exit_status);
    }

    Glib::spawn_command_line_sync(release, nullptr, nullptr, &exit_status);
    if (exit_status != EXIT_SUCCESS)
    {
        logger::error("mouse::left_click() release failed with code '{}'", exit_status);
        std::exit(exit_status);
    }

    if (double_click)
    {
        left_click(false);
    }
}

void
mouse::right_click() noexcept
{
    const auto press = "swaymsg 'seat \"seat0\" cursor press button3'";
    const auto release = "swaymsg 'seat \"seat0\" cursor release button3'";

    std::int32_t exit_status = EXIT_SUCCESS;
    Glib::spawn_command_line_sync(press, nullptr, nullptr, &exit_status);
    if (exit_status != EXIT_SUCCESS)
    {
        logger::error("mouse::right_click() press failed with code '{}'", exit_status);
        std::exit(exit_status);
    }

    Glib::spawn_command_line_sync(release, nullptr, nullptr, &exit_status);
    if (exit_status != EXIT_SUCCESS)
    {
        logger::error("mouse::right_click() release failed with code '{}'", exit_status);
        std::exit(exit_status);
    }
}
