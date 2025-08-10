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
#include <source_location>
#include <string>

#include <glibmm.h>

#include <CLI/CLI.hpp>

#include <ztd/ztd.hxx>

#include "logger/logger.hxx"

#include "commandline/commandline.hxx"

#include "vfs/env.hxx"
#include "vfs/execute.hxx"

const auto package = package_data{
    std::source_location::current().file_name(),
    "2024-05-19",
    "5.0.0",
};

int
main(int argc, char** argv)
{
    CLI::App app{"Install Kernel Source"};

    auto opt = commandline_opt_data::create(package);

    std::string kernel = "gentoo";
    static constexpr std::array<std::string, 3> kernels = {"gentoo", "git", "vanilla"};
    app.add_option("-k,--kernel", kernel, "Set install kernel")
        ->expected(1)
        ->check(CLI::IsMember(kernels));

    bool verbose = false;
    app.add_flag("--verbose", verbose, "Enable verbose emerge");

    setup_common_commandline(app, opt, false);

    CLI11_PARSE(app, argc, argv);

    vfs::env::check_running_user(vfs::env::only_run_as::root);

    std::string kernel_ebuild;
    if (kernel == "gentoo")
    {
        kernel_ebuild = "sys-kernel/gentoo-sources";
    }
    else if (kernel == "git")
    {
        kernel_ebuild = "sys-kernel/git-sources";
    }
    else // if (kernel == "vanilla")
    {
        kernel_ebuild = "sys-kernel/vanilla-sources";
    }

    { // Install kernel
        auto result =
            vfs::execute::command_line_sync("emerge --ignore-default-opts --oneshot {} {}",
                                            verbose ? "--verbose" : "--quiet",
                                            kernel_ebuild);
        if (result.exit_status != EXIT_SUCCESS)
        {
            logger::critical("Kernel install failed");
            std::exit(result.exit_status);
        }
    }

    if (std::filesystem::exists("/usr/src/linux") && std::filesystem::exists("/proc/config.gz"))
    { // Install kernel config
        if (std::filesystem::exists("/usr/src/linux/.config"))
        {
            logger::critical("Kernel config already exists, aborting");
            std::exit(EXIT_FAILURE);
        }

        auto result = vfs::execute::command_line_sync(
            "bash -c \"zcat /proc/config.gz > /usr/src/linux/.config\"");
        if (result.exit_status != EXIT_SUCCESS)
        {
            logger::critical("Kernel config install failed");
            std::exit(result.exit_status);
        }
    }

    std::exit(EXIT_SUCCESS);
}
