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

#include <filesystem>

#include <print>

#include <CLI/CLI.hpp>

#include <ztd/ztd.hxx>
#include <ztd/ztd_logger.hxx>

#include "lib/commandline.hxx"

const std::shared_ptr<commandline_opt_data>
commandline_opt_data::create(const package_data& package) noexcept
{
    return std::make_shared<commandline_opt_data>(package);
}

commandline_opt_data::commandline_opt_data(const package_data& package) noexcept
{
    this->package = package;
}

void
run_commandline(const std::shared_ptr<commandline_opt_data>& opt)
{
    if (opt->version)
    {
        std::println("{} {}", opt->package.source_path.filename().string(), opt->package.version);
        std::exit(EXIT_SUCCESS);
    }

    if (opt->loglevel == "trace")
    {
        ztd::logger::initialize(spdlog::level::trace, opt->logfile);
    }
    else if (opt->loglevel == "debug")
    {
        ztd::logger::initialize(spdlog::level::debug, opt->logfile);
    }
    else if (opt->loglevel == "info")
    {
        ztd::logger::initialize(spdlog::level::info, opt->logfile);
    }
    else if (opt->loglevel == "warning")
    {
        ztd::logger::initialize(spdlog::level::warn, opt->logfile);
    }
    else if (opt->loglevel == "error")
    {
        ztd::logger::initialize(spdlog::level::err, opt->logfile);
    }
    else if (opt->loglevel == "critical")
    {
        ztd::logger::initialize(spdlog::level::critical, opt->logfile);
    }
    else
    {
        ztd::logger::initialize(spdlog::level::off);
    }
}

void
setup_common_commandline(CLI::App& app, const std::shared_ptr<commandline_opt_data>& opt,
                         const bool file_list)
{
    const std::array<std::string, 8> loglevels =
        {"trace", "debug", "info", "warning", "error", "critical", "off"};
    app.add_option("--loglevel", opt->loglevel, "Set the loglevel")
        ->expected(1)
        ->check(CLI::IsMember(loglevels));

    const auto is_absolute_path = CLI::Validator(
        [](const std::filesystem::path& input)
        {
            if (input.is_absolute())
            {
                return std::string();
            }
            return std::format("Logfile path must be absolute: {}", input.string());
        },
        "");
    app.add_option("--logfile", opt->logfile, "absolute path to the logfile")
        ->expected(1)
        ->check(is_absolute_path);

    app.add_flag("-v,--version", opt->version, "Show version information");

    // Everything else
    if (file_list)
    {
        app.add_option("files", opt->files, "File list")->expected(0, -1);
    }

    app.callback([&opt]() { run_commandline(opt); });
}
