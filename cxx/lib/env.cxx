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

#include <print>

#include <cstdlib>

#include <unistd.h>

#include "lib/env.hxx"

void
env::check_running_user(const only_run_as user) noexcept
{
    const bool is_root = geteuid() == 0;
    if (user == only_run_as::root)
    {
        if (!is_root)
        {
            std::println("Requires root, exiting");
            std::exit(EXIT_FAILURE);
        }
    }
    else if (user == only_run_as::user)
    {
        if (is_root)
        {
            std::println("Do not run as root, exiting");
            std::exit(EXIT_FAILURE);
        }
    }
}

bool
env::is_wayland() noexcept
{
    const char* wayland = std::getenv("WAYLAND_DISPLAY");
    return wayland != nullptr;
}
