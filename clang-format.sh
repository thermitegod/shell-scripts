#!/bin/bash

find ./cxx -maxdepth 1 -type f -o -iname *.hxx -o -iname *.cxx -o -iname *.ixx | xargs clang-format -i
find ./cxx/lib -maxdepth 1 -type f -o -iname *.hxx -o -iname *.cxx -o -iname *.ixx | xargs clang-format -i
