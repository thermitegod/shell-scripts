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

#include <glibmm.h>

#include "lib/user-dirs.hxx"

const std::filesystem::path
user::desktop_dir() noexcept
{
    return Glib::get_user_special_dir(Glib::UserDirectory::DESKTOP);
}

const std::filesystem::path
user::documents_dir() noexcept
{
    return Glib::get_user_special_dir(Glib::UserDirectory::DOCUMENTS);
}

const std::filesystem::path
user::download_dir() noexcept
{
    return Glib::get_user_special_dir(Glib::UserDirectory::DOWNLOAD);
}

const std::filesystem::path
user::music_dir() noexcept
{
    return Glib::get_user_special_dir(Glib::UserDirectory::MUSIC);
}

const std::filesystem::path
user::pictures_dir() noexcept
{
    return Glib::get_user_special_dir(Glib::UserDirectory::PICTURES);
}

const std::filesystem::path
user::public_share_dir() noexcept
{
    return Glib::get_user_special_dir(Glib::UserDirectory::PUBLIC_SHARE);
}

const std::filesystem::path
user::template_dir() noexcept
{
    return Glib::get_user_special_dir(Glib::UserDirectory::TEMPLATES);
}

const std::filesystem::path
user::videos_dir() noexcept
{
    return Glib::get_user_special_dir(Glib::UserDirectory::VIDEOS);
}

const std::filesystem::path
user::home_dir() noexcept
{
    return Glib::get_home_dir();
}

const std::filesystem::path
user::cache_dir() noexcept
{
    return Glib::get_user_cache_dir();
}

const std::filesystem::path
user::data_dir() noexcept
{
    return Glib::get_user_data_dir();
}

const std::filesystem::path
user::config_dir() noexcept
{
    return Glib::get_user_config_dir();
}

const std::filesystem::path
user::runtime_dir() noexcept
{
    return Glib::get_user_runtime_dir();
}
