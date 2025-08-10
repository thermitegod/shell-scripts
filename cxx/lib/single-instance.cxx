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

#include <filesystem>
#include <format>
#include <fstream>
#include <string>

#include <cstdlib>

#include <signal.h>

#include <ztd/ztd.hxx>

#include "logger/logger.hxx"

#include "lib/file-ops.hxx"
#include "lib/proc.hxx"
#include "lib/single-instance.hxx"
#include "lib/user-dirs.hxx"

const std::filesystem::path
get_pid_path() noexcept
{
    return user::runtime_dir() / std::format("{}.pid", proc::self::name());
}

void
single_instance_finalize() noexcept
{
    const auto pid_path = get_pid_path();
    if (std::filesystem::exists(pid_path))
    {
        std::filesystem::remove(pid_path);
    }
}

bool
is_process_running(pid_t pid) noexcept
{
    // could add another check here to make sure pid has
    // not been reissued in case of a stale pid file.
    return (::kill(pid, 0) == 0);
}

void
create_single_instance() noexcept
{
    std::atexit(single_instance_finalize);

    const auto path = get_pid_path();
    if (!std::filesystem::exists(path))
    {
        return;
    }

    std::ifstream pid_file(path);
    if (pid_file)
    {
        pid_t pid;
        pid_file >> pid;
        pid_file.close();

        if (is_process_running(pid))
        {
            logger::error("single instance check failed for '{}'", proc::self::name());
            std::exit(EXIT_FAILURE);
        }
    }

    // use std::to_string to avoid locale formating of pid
    // from '12345' -> '12,345'
    const auto ec = lib::write_file(path, std::to_string(::getpid()));
    logger::critical_if(bool(ec), "Failed to write pid file: {} {}", path.string(), ec.message());
}
