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

#include <glibmm.h>

#include "lib/user-dirs.hxx"

const std::string
user::desktop_dir() noexcept
{
    return Glib::get_user_special_dir(Glib::UserDirectory::DESKTOP);
}

const std::string
user::documents_dir() noexcept
{
    return Glib::get_user_special_dir(Glib::UserDirectory::DOCUMENTS);
}

const std::string
user::download_dir() noexcept
{
    return Glib::get_user_special_dir(Glib::UserDirectory::DOWNLOAD);
}

const std::string
user::music_dir() noexcept
{
    return Glib::get_user_special_dir(Glib::UserDirectory::MUSIC);
}

const std::string
user::pictures_dir() noexcept
{
    return Glib::get_user_special_dir(Glib::UserDirectory::PICTURES);
}

const std::string
user::public_share_dir() noexcept
{
    return Glib::get_user_special_dir(Glib::UserDirectory::PUBLIC_SHARE);
}

const std::string
user::template_dir() noexcept
{
    return Glib::get_user_special_dir(Glib::UserDirectory::TEMPLATES);
}

const std::string
user::videos_dir() noexcept
{
    return Glib::get_user_special_dir(Glib::UserDirectory::VIDEOS);
}

const std::string
user::home_dir() noexcept
{
    return Glib::get_home_dir();
}

const std::string
user::cache_dir() noexcept
{
    return Glib::get_user_cache_dir();
}

const std::string
user::data_dir() noexcept
{
    return Glib::get_user_data_dir();
}

const std::string
user::config_dir() noexcept
{
    return Glib::get_user_config_dir();
}

const std::string
user::runtime_dir() noexcept
{
    return Glib::get_user_runtime_dir();
}
