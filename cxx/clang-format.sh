#!/bin/bash

# ./src
find ./src -maxdepth 1 -type f -o -iname *.hxx -o -iname *.cxx -o -iname *.ixx | xargs clang-format -i
