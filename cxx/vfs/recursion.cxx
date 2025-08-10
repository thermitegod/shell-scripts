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
#include <span>
#include <vector>

#include <ztd/ztd.hxx>

#include "vfs/recursion.hxx"

vfs::recursion::find_files::find_files(const std::filesystem::path& path, const i32 max_depth)
    : start_path_(path), max_depth_(max_depth)
{
    this->recursive_find_files(this->start_path_);
}

void
vfs::recursion::find_files::recursive_find_files(const std::filesystem::path& path) noexcept
{
    this->total_descent_ += 1;
    this->current_depth_ += 1;

    if (!std::filesystem::is_directory(path))
    {
        return;
    }

    for (const auto& entry : std::filesystem::directory_iterator(path))
    {
        if (entry.is_directory())
        {
            this->only_dir_list_.push_back(entry.path());

            if (this->current_depth_ == this->max_depth_)
            {
                continue;
            }

            recursive_find_files(entry.path().string());
            this->current_depth_ -= 1;
            continue;
        }

        if (entry.is_regular_file())
        {
            this->only_file_list_.push_back(entry.path());
            continue;
        }
    }
}

const std::span<const std::filesystem::path>
vfs::recursion::find_files::only_files() const noexcept
{
    return this->only_file_list_;
}

const std::span<const std::filesystem::path>
vfs::recursion::find_files::only_dirs() const noexcept
{
    return this->only_dir_list_;
}

const std::span<const std::filesystem::path>
vfs::recursion::find_files::all_entries() const noexcept
{
    return this->file_dir_list_;
}

usize
vfs::recursion::find_files::total_descent() const noexcept
{
    return this->total_descent_;
}
