#!/bin/bash

#CC=gcc CXX=g++ meson setup --prefix=${HOME}/.local --buildtype=debug ./build
#CC=gcc CXX=g++ meson setup --prefix=${HOME}/.local --buildtype=release ./build

#CC=clang CXX=clang++ meson setup --prefix=${HOME}/.local --buildtype=debug ./build
#CC=clang CXX=clang++ meson setup --prefix=${HOME}/.local --buildtype=release ./build

#CC=clang CXX=clang++ meson setup --prefix=${HOME}/.local --buildtype=debug -Db_sanitize=undefined -Db_lundef=false ./build
#CC=clang CXX=clang++ meson setup --prefix=${HOME}/.local --buildtype=debug -Db_sanitize=address -Db_lundef=false ./build
#CC=clang CXX=clang++ meson setup --prefix=${HOME}/.local --buildtype=debug -Db_sanitize=address,undefined -Db_lundef=false ./build

CC=clang CXX=clang++ meson setup ./build \
    --prefix=${HOME}/.local \
    --buildtype=debugoptimized \
    -Db_lto=true -Db_lto_mode=thin -Db_thinlto_cache=true
    # -Db_sanitize=address -Db_lundef=false \
