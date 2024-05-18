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

#include <print>

#include <filesystem>

#include <vector>

#include <source_location>

#include <glibmm.h>

#include <CLI/CLI.hpp>

#include <ztd/ztd.hxx>
#include <ztd/ztd_logger.hxx>

#include "lib/commandline.hxx"

const auto package = package_data{
    std::source_location::current().file_name(),
    "2024-05-17",
    "2.0.0",
};

int
main(int argc, char** argv)
{
    CLI::App app{"Regenerate Ebuild Manifest"};

    auto opt = commandline_opt_data::create(package);

    setup_common_commandline(app, opt, false);

    CLI11_PARSE(app, argc, argv);

    std::vector<std::filesystem::path> ebuilds;
    for (const auto& dfile : std::filesystem::directory_iterator(std::filesystem::current_path()))
    {
        const auto file = dfile.path();
        if (file.extension() == ".ebuild")
        {
            ebuilds.push_back(file);
        }
    }

    if (ebuilds.empty())
    {
        std::println("Failed to find an ebuild");
        std::exit(EXIT_FAILURE);
    }
    ztd::logger::debug("Ebuilds found '{}' ", ebuilds.size());

    std::ranges::sort(ebuilds);

    const auto command = std::format("ebuild {} manifest", ebuilds.back().string());
    ztd::logger::debug("COMMAND({})", command);

    i32 exit_status = EXIT_SUCCESS;
    Glib::spawn_command_line_sync(command, nullptr, nullptr, &exit_status);
    std::exit(exit_status);
}
