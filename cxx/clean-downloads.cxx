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
#include <source_location>
#include <string>
#include <string_view>
#include <utility>
#include <vector>

#include <CLI/CLI.hpp>

#include <ztd/ztd.hxx>

#include "logger/logger.hxx"

#include "commandline/commandline.hxx"

#include "vfs/hash.hxx"
#include "vfs/user-dirs.hxx"

const auto package = package_data{
    std::source_location::current().file_name(),
    "2024-01-04",
    "1.0.0",
};

int
main(int argc, char** argv)
{
    CLI::App app{"TEST"};

    std::filesystem::path run_path = vfs::user::download();
    app.add_option("-p,--path",
                   run_path,
                   std::format("Path to run in, default [{}]", run_path.string()));

    bool disable_delete = false;
    app.add_option("-D,--no-delete", disable_delete, "Do not delete duplicate files");

    auto opt = commandline_opt_data::create(package);

    setup_common_commandline(app, opt, false);

    CLI11_PARSE(app, argc, argv);

    // logic

    // files in dir
    std::vector<std::filesystem::path> file_list;
    // files in dir that have chrome dup name marker
    std::vector<std::pair<std::filesystem::path, std::filesystem::path>> file_dup_name_only_list;
    // files in dir that have chrome dup name marker but
    // no file without a marker exists
    std::vector<std::filesystem::path> file_not_dup_list;

    const std::vector<std::string> chrome_dup_markers =
        {" (1)", " (2)", " (3)", " (4)", " (5)", " (6)", " (7)", " (8)", " (9)"};

    if (!std::filesystem::is_directory(run_path))
    {
        if (!std::filesystem::exists(run_path))
        {
            logger::error("No such directory [{}]", run_path.string());
        }
        else
        {
            logger::error("Path must be a directory [{}]", run_path.string());
        }
        std::exit(EXIT_FAILURE);
    }

    for (const auto& entry : std::filesystem::directory_iterator(run_path))
    {
        if (entry.is_directory())
        {
            continue;
        }

        const std::filesystem::path file = entry.path();
        // logger::info("path : {}", file.string());
        file_list.push_back(file);
    }

    for (const auto& file : file_list)
    {
        bool contains = false;
        for (std::string_view chrome_dup_marker : chrome_dup_markers)
        {
            if (file.string().contains(chrome_dup_marker))
            {
                contains = true;
                break;
            }
        }
        if (!contains)
        {
            continue;
        }

        std::filesystem::path file_orig = file;
        for (const std::string_view chrome_dup_marker : chrome_dup_markers)
        {
            file_orig = ztd::replace(file_orig.string(), chrome_dup_marker, "");
        }

        if (std::filesystem::exists(file_orig))
        {
            bool hash_same = vfs::hash::compare_files(file_orig, file);

            if (hash_same)
            {
                if (!disable_delete)
                {
                    // logger::info("Files same [{}] [{}]", file_orig.string(), file.string());

                    logger::info("delete: {}", file.string());
                    std::filesystem::remove(file);
                    if (std::filesystem::exists(file))
                    {
                        logger::error("Failed to delete: {}", file.string());
                        std::exit(EXIT_FAILURE);
                    }
                }
                else
                {
                    logger::info("[PRETEND] delete: {}", file.string());
                }
            }
            else
            {
                file_dup_name_only_list.push_back({file_orig, file});
            }
        }
        else
        {
            file_not_dup_list.push_back(file);
        }
    }

    if (file_dup_name_only_list.size())
    {
        logger::info("== Name Collisions, Different Files ==");
        for (const auto& files : file_dup_name_only_list)
        {
            // logger::info("[{}] | [{}]", files.first.string(), files.second.string());
            logger::info("{}", files.second.string());
        }
    }

    if (file_not_dup_list.size())
    {
        logger::info("== Name Contains Unneeded Duplicate Marker ==");
        for (const auto& file : file_not_dup_list)
        {
            logger::info("{}", file.string());
        }
    }

    std::exit(EXIT_SUCCESS);
}
