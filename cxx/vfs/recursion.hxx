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

#include <filesystem>
#include <span>
#include <vector>

#include <ztd/ztd.hxx>

namespace vfs::recursion
{
class find_files
{
  public:
    find_files() = delete;
    find_files(const std::filesystem::path& path, const i32 max_depth = -1);

    /**
     * @brief only_files
     *
     * - Get vector of only files in and below a directory.
     *
     * @return vector of file paths
     */
    const std::span<const std::filesystem::path> only_files() const noexcept;

    /**
     * @brief only_dirs
     *
     * - Get vector of files and dirs in and below a directory.
     * All other file types are ignored
     *
     * @return vector of dir paths
     */
    const std::span<const std::filesystem::path> only_dirs() const noexcept;

    /**
     * @brief all_entries
     *
     * - Get vector of files and dirs in and below a directory.
     * All other file types are ignored
     *
     * @return vector of dir paths
     */
    const std::span<const std::filesystem::path> all_entries() const noexcept;

    /**
     * @brief total_descent
     *
     * - Total number of nodes descended
     *
     * @return descent count
     */
    usize total_descent() const noexcept;

  private:
    void recursive_find_files(const std::filesystem::path& path) noexcept;

    std::filesystem::path start_path_;
    i32 max_depth_{0};
    i32 current_depth_{0};
    usize total_descent_{0};

    std::vector<std::filesystem::path> only_file_list_;
    std::vector<std::filesystem::path> only_dir_list_;
    std::vector<std::filesystem::path> file_dir_list_;
};
} // namespace vfs::recursion
