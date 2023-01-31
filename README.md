Builder - simple python script for building C/C++ projects.
It is parsing all "#include"'s from project files and passing them to gcc/g++.

# Usage
build.py main_file [options]

Options:
 - -h --help Get help about usage
 - -o <output> Set output file name
 - --compiler_flags=<flags> Pass flags directly to the compiler
