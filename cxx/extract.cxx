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
#include <print>
#include <source_location>
#include <string>

#include <glibmm.h>

#include <CLI/CLI.hpp>

#include <ztd/ztd.hxx>

#include "logger/logger.hxx"

#include "commandline/commandline.hxx"

#include "vfs/execute.hxx"

const auto package = package_data{
    std::source_location::current().file_name(),
    "2024-01-05",
    "3.0.0",
};

int
main(int argc, char** argv)
{
    CLI::App app{"Extract Archives"};

    // bool files = false;
    // app.add_flag("-f,--files", files, "decompress all files in cwd");

    // std::filesystem::path output_path;
    // app.add_option("-o,--output-dir", output_path, "extract the archive[s] in this directory")
    //     ->expected(1);

    // bool extract_to_subdir = false;
    // app.add_flag("-s,--no-subdir",
    //              extract_to_subdir,
    //              "Extract files to output dir without creating sub directories, req -o");

    auto opt = commandline_opt_data::create(package);

    setup_common_commandline(app, opt);

    CLI11_PARSE(app, argc, argv);

    if (argc == 1)
    {
        std::println("{}", app.help());
        std::exit(EXIT_SUCCESS);
    }

    for (const auto& filename : opt->files)
    {
        std::filesystem::path path = std::filesystem::absolute(filename);

        std::string command;
        if (filename.string().ends_with(".tar.bz2") || filename.string().ends_with(".tbz2"))
        {
            command = std::format("tar -xvjf \"{}\"", path.string());
        }
        else if (filename.string().ends_with(".tar.gz") || filename.string().ends_with(".tgz"))
        {
            command = std::format("tar -xvzf \"{}\"", path.string());
        }
        else if (filename.string().ends_with(".tar.xz") || filename.string().ends_with(".txz"))
        {
            command = std::format("tar -xvJf \"{}\"", path.string());
        }
        else if (filename.string().ends_with(".tar.zst"))
        {
            command = std::format("zstd -dc --long=31 \"{}\" | tar xvf -", path.string());
        }
        else if (filename.string().ends_with(".tar.lz4"))
        {
            command = std::format("lz4 -dc \"{}\" | tar xvf -", path.string());
        }
        else if (filename.string().ends_with(".tar.lzma"))
        {
            command = std::format("tarlzma -xvf \"{}\"", path.string());
        }
        else if (filename.string().ends_with(".tar.lzr"))
        {
            command = std::format("lrzuntar \"{}\"", path.string());
        }
        else if (filename.string().ends_with(".rar") || filename.string().ends_with(".RAR") ||
                 filename.string().ends_with(".cbr"))
        {
            command = std::format("unrar \"{}\"", path.string());
        }
        else if (filename.string().ends_with(".gz"))
        {
            command = std::format("gunzip -k \"{}\"", path.string());
        }
        else if (filename.string().ends_with(".xz"))
        {
            command = std::format("unxz -k \"{}\"", path.string());
        }
        else if (filename.string().ends_with(".bz2"))
        {
            command = std::format("bzip2 -dk \"{}\"", path.string());
        }
        else if (filename.string().ends_with(".zst"))
        {
            command = std::format("unzstd -d --long=31 \"{}\"", path.string());
        }
        else if (filename.string().ends_with(".tar"))
        {
            command = std::format("tar -xvf \"{}\"", path.string());
        }
        else if (filename.string().ends_with(".zip") || filename.string().ends_with(".cbz"))
        {
            command = std::format("unzip \"{}\"", path.string());
        }
        else if (filename.string().ends_with(".7z") || filename.string().ends_with(".iso") ||
                 filename.string().ends_with(".ISO"))
        {
            command = std::format("7zz x \"{}\"", path.string());
        }
        else
        {
            logger::error("cannot extract: {}", path.string());
        }

        auto result = vfs::execute::command_line_sync(command);
        if (result.exit_status != EXIT_SUCCESS)
        {
            logger::error("{}", result.standard_error);
            break;
        }
    }

    std::exit(EXIT_SUCCESS);
}
