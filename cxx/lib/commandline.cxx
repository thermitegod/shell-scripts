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
#include <print>

#include <CLI/CLI.hpp>

#include <ztd/ztd.hxx>

#include "logger/logger.hxx"

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

static void
run_commandline(const std::shared_ptr<commandline_opt_data>& opt) noexcept
{
    if (opt->version)
    {
        std::println("{} {}", opt->package.source_path.filename().string(), opt->package.version);
        std::exit(EXIT_SUCCESS);
    }

    logger::initialize(opt->log_levels, opt->logfile);
}

void
setup_common_commandline(CLI::App& app, const std::shared_ptr<commandline_opt_data>& opt,
                         const bool file_list)
{
    app.add_option("--loglevel", opt->raw_log_levels, "Set the loglevel. Format: domain=level")
        ->check(
            [&opt](const auto& value)
            {
                constexpr auto log_levels = magic_enum::enum_names<spdlog::level::level_enum>();
                constexpr auto valid_domains = magic_enum::enum_names<logger::domain>();

                const auto pos = value.find('=');
                if (pos == std::string::npos)
                {
                    return std::string("Must be in format domain=level");
                }

                const auto domain = value.substr(0, pos);
                if (!std::ranges::contains(valid_domains, domain))
                {
                    return std::format("Invalid domain: {}", domain);
                }

                const auto level = value.substr(pos + 1);
                if (!std::ranges::contains(log_levels, level))
                {
                    return std::format("Invalid log level: {}", level);
                }

                opt->log_levels.insert({domain, level});

                return std::string();
            });

    app.add_option("--logfile", opt->logfile, "absolute path to the logfile")
        ->expected(1)
        ->check(
            [](const std::filesystem::path& input)
            {
                if (input.is_absolute())
                {
                    return std::string();
                }
                return std::format("Logfile path must be absolute: {}", input.string());
            });

    app.add_flag("-v,--version", opt->version, "Show version information");

    // Everything else
    if (file_list)
    {
        app.add_option("FILES", opt->files, "File list")->expected(0, -1);
    }

    app.callback([&opt]() { run_commandline(opt); });
}
