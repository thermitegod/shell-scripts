/**
 * Copyright (C) 2025 Brandon Zorn <brandonzorn@cock.li>
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

#include <algorithm>
#include <filesystem>
#include <print>
#include <source_location>
#include <string>
#include <string_view>
#include <utility>
#include <vector>

#include <glibmm.h>

#include <CLI/CLI.hpp>

#include <ztd/detail/string_python.hxx>
#include <ztd/ztd.hxx>

#include "commandline/commandline.hxx"

#include "vfs/recursion.hxx"
#include "vfs/tools.hxx"

const auto package = package_data{
    std::source_location::current().file_name(),
    "2025-08-10",
    "2.0.0",
};

enum class filetype
{
    archive,
    image,
    video
};

// clang-format off
std::vector<std::string_view> ext_archive{
    ".zip",
    ".7z",
    ".rar",
    ".cbr",
    ".cbz",
    ".cb7",
    ".tar",
    ".tar.bz2",
    ".tar.gz",
    ".tar.lz4",
    ".tar.lzo",
    ".tar.xz",
    ".tar.zst",
    ".bz2",
    ".gz",
    ".lz4",
    ".lzo",
    ".xz",
    ".zst",
};

std::vector<std::string_view> ext_image{
    ".png",
    ".jpg",
    ".jpeg",
    ".jxl",
    ".jpe",
    ".gif",
    ".bmp",
    ".ico",
};

std::vector<std::string_view> ext_video{
    ".webm",
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".wmv",
};
// clang-format on

static const auto exts = [](filetype type)
{
    if (type == filetype::archive)
    {
        return ext_archive;
    }
    else if (type == filetype::image)
    {
        return ext_image;
    }
    else if (type == filetype::video)
    {
        return ext_video;
    }
    std::unreachable();
};

void
count_files(const std::filesystem::path& path, filetype type) noexcept
{
    u64 counter;
    u64 counter_total;

    std::vector<std::filesystem::path> file_list_done;

    auto file_list = vfs::recursion::find_files(std::filesystem::current_path()).only_files();
    if (file_list.empty())
    {
        std::println("No files in: {}", path.string());
        return;
    }

    for (const auto& ext : exts(type))
    {
        for (const auto& file : file_list)
        {
            if (std::ranges::contains(file_list_done, file))
            {
                continue;
            }

            if (vfs::split_basename_extension(file).extension == ext)
            {
                counter += 1;
                file_list_done.push_back(file);
            }
        }

        if (counter != 0)
        {
            std::println("{} \t: {}", ztd::ljust(ztd::upper(ext), 10), counter);
            counter_total += counter;
            counter = 0;
        }
    }

    if (counter_total != 0)
    {
        std::println("Total\t\t: {}", counter_total);
    }
}

void
list_files(const std::filesystem::path& path, filetype type) noexcept
{
    auto file_list = vfs::recursion::find_files(std::filesystem::current_path()).only_files();
    if (file_list.empty())
    {
        std::println("No files in: {}", path.string());
        return;
    }

    for (const auto& ext : exts(type))
    {
        std::println("Listing all of: {}", ztd::upper(ext));
        for (const auto& file : file_list)
        {
            if (vfs::split_basename_extension(file).extension == ext)
            {
                std::println("{}", file.string());
            }
        }
    }
}

int
main(int argc, char** argv)
{
    CLI::App app{"Count types of files"};

    bool list = false;
    app.add_flag("-l,--list", list, "List files that match patern");

    auto opt = commandline::opt_data::create(package);

    commandline::create_common(app, opt, false);

    CLI11_PARSE(app, argc, argv);

    const auto name = ztd::rpartition(argv[0], "/")[2];
    auto type = [](std::string_view name)
    {
        if (name == "count-archive")
        {
            return filetype::archive;
        }
        else if (name == "count-image")
        {
            return filetype::image;
        }
        else if (name == "count-video")
        {
            return filetype::video;
        }
        std::unreachable();
    }(name);

    if (list)
    {
        list_files(std::filesystem::current_path(), type);
    }
    else
    {
        count_files(std::filesystem::current_path(), type);
    }

    std::exit(EXIT_SUCCESS);
}
