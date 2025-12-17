#!/usr/bin/env bash

find \
    ./cxx \
    -iname '*.cxx' -o -iname '*.hxx' | \
    clang-format -i --files=/dev/stdin
