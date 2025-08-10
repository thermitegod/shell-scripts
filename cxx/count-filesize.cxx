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

#include <glibmm.h>

#include <CLI/CLI.hpp>

#include <ztd/ztd.hxx>

#include "commandline/commandline.hxx"

#include "vfs/recursion.hxx"

const auto package = package_data{
    std::source_location::current().file_name(),
    "2025-08-10",
    "2.0.0",
};

struct ranges_data
{
    ztd::byte_iec lower;
    ztd::byte_iec upper;
};

using namespace ztd::byte_iec_literals;

std::array<ranges_data, 8> default_ranges{{
    {
        0_B,
        10_MiB,
    },
    {
        10_MiB,
        100_MiB,
    },
    {
        100_MiB,
        150_MiB,
    },
    {
        150_MiB,
        200_MiB,
    },
    {
        200_MiB,
        500_MiB,
    },
    {
        500_MiB,
        1_GiB,
    },
    {
        1_GiB,
        10_GiB,
    },
    {
        10_GiB,
        100_GiB,
    },
}};

void
count(const std::filesystem::path& path) noexcept
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

    for (const auto& range_data : default_ranges)
    {
        for (const auto& file : file_list)
        {
            if (std::ranges::contains(file_list_done, file))
            {
                continue;
            }

            const auto stat = ztd::statx::create(file);
            if (!stat)
            {
                continue;
            }
            auto size = ztd::byte_iec((*stat).size());

            if (size >= range_data.lower && size <= range_data.upper)
            {
                counter += 1;
                file_list_done.push_back(file);
            }
        }

        if (counter != 0)
        {
            std::println(
                "{} \t: {}",
                ztd::ljust(
                    std::format("{} - {}", range_data.lower.format(0), range_data.upper.format(0)),
                    10),
                counter);
            counter_total += counter;
            counter = 0;
        }
    }

    if (counter_total != 0)
    {
        std::println("Total\t\t: {}", counter_total);
    }
}

int
main(int argc, char** argv)
{
    CLI::App app{"Count filesizes in size ranges"};

    auto opt = commandline::opt_data::create(package);

    commandline::create_common(app, opt, false);

    CLI11_PARSE(app, argc, argv);

    count(std::filesystem::current_path());

    std::exit(EXIT_SUCCESS);
}
