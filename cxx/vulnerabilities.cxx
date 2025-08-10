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

#include <source_location>

#include <CLI/CLI.hpp>

#include <ztd/ztd.hxx>

#include "lib/commandline.hxx"
#include "lib/colors.hxx"

const auto package = package_data{
    std::source_location::current().file_name(),
    "2024-05-17",
    "2.0.0",
};

int
main(int argc, char** argv)
{
    CLI::App app{"Print CPU Vulnerabilities"};

    auto opt = commandline_opt_data::create(package);

    setup_common_commandline(app, opt, false);

    CLI11_PARSE(app, argc, argv);

    usize width = 0;
    for (const auto& entry :
         std::filesystem::directory_iterator("/sys/devices/system/cpu/vulnerabilities"))
    {
        const auto filename = entry.path().filename();
        if (filename.string().size() > width)
        {
            width = filename.string().size();
        }
    }

    for (const auto& entry :
         std::filesystem::directory_iterator("/sys/devices/system/cpu/vulnerabilities"))
    {
        const auto filename = entry.path().filename();

        std::ifstream file(entry.path());
        std::string state;
        std::getline(file, state);
        file.close();

        std::println("{}{}{} : {}",
                     colors::yel,
                     ztd::rjust(filename.string(), width),
                     colors::nc,
                     ztd::strip(state));
    }

    std::exit(EXIT_SUCCESS);
}
