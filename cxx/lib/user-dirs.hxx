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

namespace user
{
const std::filesystem::path desktop_dir() noexcept;
const std::filesystem::path documents_dir() noexcept;
const std::filesystem::path download_dir() noexcept;
const std::filesystem::path music_dir() noexcept;
const std::filesystem::path pictures_dir() noexcept;
const std::filesystem::path public_share_dir() noexcept;
const std::filesystem::path template_dir() noexcept;
const std::filesystem::path videos_dir() noexcept;

const std::filesystem::path home_dir() noexcept;
const std::filesystem::path cache_dir() noexcept;
const std::filesystem::path data_dir() noexcept;
const std::filesystem::path config_dir() noexcept;
const std::filesystem::path runtime_dir() noexcept;
} // namespace user
