#!/bin/bash

find ./cxx -iname '*.cxx' -o -iname '*.hxx' | xargs --max-args=$(nproc) clang-format -i
