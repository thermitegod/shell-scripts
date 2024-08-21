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

#include <memory>

#include <CLI/CLI.hpp>

#include <ztd/ztd.hxx>

struct package_data
{
    std::filesystem::path source_path;
    std::string date;
    std::string version;
};

struct commandline_opt_data : public std::enable_shared_from_this<commandline_opt_data>
{
    commandline_opt_data() = delete;
    commandline_opt_data(const package_data& package) noexcept;
    static const std::shared_ptr<commandline_opt_data> create(const package_data& package) noexcept;

    std::vector<std::string> raw_log_levels;
    std::unordered_map<std::string, std::string> log_levels;
    // std::filesystem::path logfile{"/tmp/test.log"};
    std::filesystem::path logfile{};

    bool version{false};
    package_data package;

    std::vector<std::filesystem::path> files{};
};

void setup_common_commandline(CLI::App& app, const std::shared_ptr<commandline_opt_data>& opt,
                              const bool file_list = true);
