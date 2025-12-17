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

#include <filesystem>
#include <print>
#include <source_location>
#include <string>

#include <cstdlib>

#include <CLI/CLI.hpp>

#include <ztd/ztd.hxx>

#include "logger/logger.hxx"

#include "commandline/commandline.hxx"

#include "vfs/execute.hxx"

const auto package = package_data{
    std::source_location::current().file_name(),
    "2025-12-16",
    "3.0.0",
};

int
main(int argc, char** argv)
{
    CLI::App app{"Convert Images"};

    std::filesystem::path directory = "";
    app.add_option("-d,--directory", directory, "Convert images in this directory")
        ->expected(1)
        ->default_val(std::filesystem::current_path());

    // std::filesystem::path output = "";
    // app.add_option("-o,--output", output, "Output path for converted file(s)")
    //     ->expected(1)
    //     ->default_val(std::filesystem::current_path() / "output");

    auto convert = app.add_option_group("Conversion Type");
    bool jpg_to_jpg = false;
    bool jpg_to_png = false;
    bool png_to_png = false;
    bool png_to_jpg = false;
    std::int32_t quality = 0;
    convert->add_flag("-J,--jpg-to-jpg", jpg_to_jpg, "Convert JPG to JPG");
    convert->add_flag("-j,--jpg-to-png", jpg_to_png, "Convert JPG to PNG");
    convert->add_flag("-P,--png-to-png", png_to_png, "Convert PNG to PNG");
    convert->add_flag("-p,--png-to-jpg", png_to_jpg, "Convert PNG to JPG");
    convert->add_option("-q,--quality", quality, "Image quality, Default: JPG(95), PNG(7)")
        ->expected(1)
        ->default_val(0);
    convert->require_option(0, 1);

    auto opt = commandline::opt_data::create(package);

    commandline::create_common(app, opt, false);

    CLI11_PARSE(app, argc, argv);

    if (argc == 1)
    {
        std::println("{}", app.help());
        std::exit(EXIT_SUCCESS);
    }

    std::filesystem::path origext;
    std::filesystem::path newext;
    if (jpg_to_jpg)
    {
        origext = ".jpg";
        newext = ".jpg";
        if (quality == 0)
        {
            quality = 95;
        }
    }
    else if (jpg_to_png)
    {
        origext = ".jpg";
        newext = ".png";
        if (quality == 0)
        {
            quality = 7;
        }
    }
    else if (png_to_png)
    {
        origext = ".png";
        newext = ".png";
        if (quality == 0)
        {
            quality = 7;
        }
    }
    else if (png_to_jpg)
    {
        origext = ".png";
        newext = ".jpg";
        if (quality == 0)
        {
            quality = 95;
        }
    }

    if (!std::filesystem::exists(directory / "output"))
    {
        std::error_code ec;
        std::filesystem::create_directories(directory / "output", ec);
        if (ec)
        {
            logger::critical("Failed to create output directory: {}", ec.message());
            std::exit(EXIT_FAILURE);
        }
    }

    for (const auto& dfile : std::filesystem::directory_iterator(directory))
    {
        const auto file = dfile.path();
        if (file.extension() == origext)
        {
            auto stem = file.stem();
            const auto output = directory / "output" / file.stem() += newext;
            // logger::info("input={}, output={}", file.string(), output.string());

            auto result = vfs::execute::command_line_sync("gm convert -quality {} {} {}",
                                                          quality,
                                                          vfs::execute::quote(file.string()),
                                                          vfs::execute::quote(output.string()));

            if (result.exit_status != 0)
            {
                logger::error("Conversion Failed: {}", result.standard_error);
                std::exit(EXIT_FAILURE);
            }

            logger::info("Done: {}", file.string());
        }
    }

    std::exit(EXIT_SUCCESS);
}
