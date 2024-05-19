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

#include <filesystem>

#include <print>

#include <source_location>

#include <glibmm.h>

#include <CLI/CLI.hpp>

#include <ztd/ztd.hxx>
#include <ztd/ztd_logger.hxx>

#include "lib/commandline.hxx"
#include "lib/env.hxx"

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

    env::check_running_user(env::only_run_as::root);

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
        const auto command = std::format("emerge --ignore-default-opts --oneshot {} {}",
                                         verbose ? "--verbose" : "--quiet",
                                         kernel_ebuild);
        ztd::logger::debug("COMMAND({})", command);

        i32 exit_status = EXIT_SUCCESS;
        Glib::spawn_command_line_sync(command, nullptr, nullptr, &exit_status);

        if (exit_status != EXIT_SUCCESS)
        {
            ztd::logger::critical("Kernel install failed");
            std::exit(exit_status);
        }
    }

    if (std::filesystem::exists("/usr/src/linux") && std::filesystem::exists("/proc/config.gz"))
    { // Install kernel config
        if (std::filesystem::exists("/usr/src/linux/.config"))
        {
            ztd::logger::critical("Kernel config already exists, aborting");
            std::exit(EXIT_FAILURE);
        }

        const auto command =
            std::format("bash -c \"zcat /proc/config.gz > /usr/src/linux/.config\"");
        ztd::logger::debug("COMMAND({})", command);

        i32 exit_status = EXIT_SUCCESS;
        Glib::spawn_command_line_sync(command, nullptr, nullptr, &exit_status);

        if (exit_status != EXIT_SUCCESS)
        {
            ztd::logger::critical("Kernel config install failed");
            std::exit(exit_status);
        }
    }

    std::exit(EXIT_SUCCESS);
}
