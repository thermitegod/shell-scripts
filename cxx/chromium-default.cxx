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

#include <format>

#include <array>

#include <source_location>

#include <glibmm.h>

#include <CLI/CLI.hpp>

#include <ztd/ztd.hxx>
#include <ztd/ztd_logger.hxx>

#include "lib/env.hxx"
#include "lib/commandline.hxx"
#include "lib/user-dirs.hxx"

const auto package = package_data{
    std::source_location::current().file_name(),
    "2024-01-04",
    "9.0.0",
};

#define LAUNCH_ASYNC

int
main(int argc, char** argv)
{
    CLI::App app{"Chrome multiple profiles launcher"};

    const std::array<std::string, 3> chrome_bins = {
        "google-chrome-stable",
        "google-chrome-unstable",
        "google-chrome-beta",
    };
    std::string chrome_bin_name = chrome_bins[0];
    app.add_option("-c,--chrome", chrome_bin_name, "chrome binary to use")
        ->expected(1)
        ->check(CLI::IsMember(chrome_bins));

    auto opt = commandline_opt_data::create(package);

    setup_common_commandline(app, opt, false);

    CLI11_PARSE(app, argc, argv);

    env::check_running_user(env::only_run_as::user);

    // need to know display server type for ozone to work
    const std::string display_server = env::is_wayland() ? "wayland" : "x11";

    // symlinks must be named 'chromium-<profile>' to work.
    // e.g. ln -s chromium-default chromium-<profile>
    const std::filesystem::path launch_name = argv[0];
    const std::string profile_name =
        ztd::removeprefix(launch_name.filename().string(), "chromium-");

    // Get chrome bin name from file path
    std::string bin_name = chrome_bin_name;
    if (bin_name.contains('/'))
    {
        bin_name = ztd::rpartition(chrome_bin_name, "/")[2];
    }

    // Build config path
    const std::string chrome_profile = std::format("{}-{}", bin_name, profile_name);
    const std::string profile_path =
        Glib::build_filename(user::config_dir(), "chrome", chrome_profile);

    // ztd::logger::info("argv[0]        = {}", argv[0]);
    // ztd::logger::info("profile_name   = {}", profile_name);
    // ztd::logger::info("chrome_profile = {}", chrome_profile);
    // ztd::logger::info("profile_path   = {}", profile_path);

    const std::string command = std::format("{} "
                                            "--user-data-dir={} "
                                            "--ozone-platform={} "
                                            "--no-default-browser-check ",
                                            chrome_bin_name,
                                            profile_path,
                                            display_server);

#if defined(LAUNCH_ASYNC)
    Glib::spawn_command_line_async(command);
    std::exit(EXIT_SUCCESS);
#else
    i32 exit_status;
    Glib::spawn_command_line_sync(command, nullptr, nullptr, &exit_status);
    std::exit(exit_status);
#endif
}
