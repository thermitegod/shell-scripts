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
#include <ztd/ztd_logger.hxx>

struct commandline_opt_data : public std::enable_shared_from_this<commandline_opt_data>
{
    std::string loglevel{"trace"};
    // std::filesystem::path logfile{"/tmp/test.log"};
    std::filesystem::path logfile{};

    bool show_version{false};
    struct version_data
    {
        std::filesystem::path source_path;
        std::string date;
        std::string version;
    };
    version_data version_data;

    std::vector<std::filesystem::path> files{};
};

using commandline_opt_data_t = std::shared_ptr<commandline_opt_data>;

void setup_common_commandline(CLI::App& app, const commandline_opt_data_t& opt,
                              const bool file_list = true);
