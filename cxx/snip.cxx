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

#include <chrono>
#include <source_location>
#include <string>

#include <glibmm.h>

#include <CLI/CLI.hpp>

#include <ztd/ztd.hxx>

#include "logger/logger.hxx"

#include "commandline/commandline.hxx"

#include "utils/single-instance.hxx"

#include "vfs/execute.hxx"
#include "vfs/user-dirs.hxx"

const auto package = package_data{
    std::source_location::current().file_name(),
    "2024-05-17",
    "8.0.0",
};

int
main(int argc, char** argv)
{
    CLI::App app{"Take Screenshots on SwayWM"};

    bool root = false;
    app.add_flag("-r,--root", root, "Screenshot window root");

    auto opt = commandline_opt_data::create(package);

    setup_common_commandline(app, opt, false);

    CLI11_PARSE(app, argc, argv);

    utils::instance::create();

    const std::filesystem::path snip_path =
        vfs::user::home() /
        std::format("{}.png",
                    std::chrono::system_clock::to_time_t(std::chrono::system_clock::now()));

    std::string command;
    if (root)
    {
        command = std::format("grimshot save screen {}", snip_path.string());
    }
    else
    {
        command = std::format("grimshot save area {}", snip_path.string());
    }

    auto result = vfs::execute::command_line_sync(command);
    std::exit(result.exit_status);
}
