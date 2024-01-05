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

#include <format>
#include <spdlog/common.h>

#if defined(__cpp_lib_print)
#include <print>
#else
#include <iostream>
#endif

#include <CLI/CLI.hpp>

#include <ztd/ztd.hxx>
#include <ztd/ztd_logger.hxx>

#include "lib/commandline.hxx"

void
run_commandline(const commandline_opt_data_t& opt)
{
    if (opt->show_version)
    {
#if defined(__cpp_lib_print)
        std::println("{} {}",
                     opt->version_data.source_path.filename().string(),
                     opt->version_data.version);
#else
        std::cout << std::format("{} {}",
                                 opt->version_data.source_path.filename().string(),
                                 opt->version_data.version)
                  << std::endl;
#endif

        std::exit(EXIT_SUCCESS);
    }

    if (opt->loglevel == "trace")
    {
        ztd::logger::initialize(spdlog::level::trace);
    }
    else if (opt->loglevel == "debug")
    {
        ztd::logger::initialize(spdlog::level::debug);
    }
    else if (opt->loglevel == "info")
    {
        ztd::logger::initialize(spdlog::level::info);
    }
    else if (opt->loglevel == "warning")
    {
        ztd::logger::initialize(spdlog::level::warn);
    }
    else if (opt->loglevel == "error")
    {
        ztd::logger::initialize(spdlog::level::err);
    }
    else if (opt->loglevel == "critical")
    {
        ztd::logger::initialize(spdlog::level::critical);
    }
    else
    {
        ztd::logger::initialize(spdlog::level::off);
    }
}

void
setup_common_commandline(CLI::App& app, const commandline_opt_data_t& opt, const bool file_list)
{
    const std::array<std::string, 8> loglevels =
        {"trace", "debug", "info", "warning", "error", "critical", "off"};
    app.add_option("-l,--loglevel", opt->loglevel, "Set the loglevel")
        ->expected(1)
        ->check(CLI::IsMember(loglevels));
    app.add_flag("-v,--version", opt->show_version, "Show version information");

    // Everything else
    if (file_list)
    {
        app.add_option("files", opt->files, "File list")->expected(0, -1);
    }

    app.callback([&opt]() { run_commandline(opt); });
}
