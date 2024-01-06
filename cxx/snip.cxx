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

#include <chrono>

#include <memory>

#include <source_location>

#include <glibmm.h>

#include <CLI/CLI.hpp>

#include <ztd/ztd.hxx>
#include <ztd/ztd_logger.hxx>

#include "lib/commandline.hxx"
#include "lib/env.hxx"
#include "lib/single-instance.hxx"
#include "lib/user-dirs.hxx"

#define PACKAGE_DATE "2024-01-05"
#define PACKAGE_VERSION "7.0.0"

int
main(int argc, char** argv)
{
    CLI::App app{"Take Screenshots"};

    bool root = false;
    app.add_flag("-r,--root", root, "Screenshot window root");

    auto opt = std::make_shared<commandline_opt_data>();
    opt->version_data = {std::source_location::current().file_name(),
                         PACKAGE_DATE,
                         PACKAGE_VERSION};
    setup_common_commandline(app, opt, false);

    CLI11_PARSE(app, argc, argv);

    create_single_instance();

    const std::filesystem::path snip_path =
        user::home_dir() /
        std::format("{}.png",
                    std::chrono::system_clock::to_time_t(std::chrono::system_clock::now()));

    std::string command;
    if (env::is_wayland())
    {
        if (root)
        {
            command = std::format("grimshot save screen {}", snip_path.string());
        }
        else
        {
            command = std::format("grimshot save area {}", snip_path.string());
        }
    }
    else
    {
        if (root)
        {
            command = std::format("gm import -window root {}", snip_path.string());
        }
        else
        {
            command = std::format("gm import {}", snip_path.string());
        }
    }

    i32 exit_status;
    Glib::spawn_command_line_sync(command, nullptr, nullptr, &exit_status);
    std::exit(exit_status);
}
