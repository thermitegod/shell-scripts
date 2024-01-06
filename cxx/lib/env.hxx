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

namespace env
{
enum class only_run_as
{
    user,
    root,
    any,
};

/**
 * @brief check_user
 *
 * - Only allow a user or root to run a command
 *
 * @param[in] user allowed user type
 */
void check_running_user(const only_run_as user) noexcept;

/**
 * @brief Is Wayland
 *
 * - Is the display server wayland
 *
 * @return true if the display server wayland, otherwise false
 */
bool is_wayland() noexcept;
} // namespace env
