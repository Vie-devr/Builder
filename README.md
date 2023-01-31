# Builder
Builder - simple python script for building C/C++ projects.
The script works by first finding all the source files that the main file depends on (recursively, if necessary), and then it passes those files, along with the include directories and compiler flags, to the gcc/g++ compiler.

## Usage
build.py main_file [options]

Options:
 - -h --help                Get help about usage
 - -o <output>              Set output file name
 - -I <directory>           Add include directory
 - --compiler_flags=<flags> Pass flags directly to the compiler
