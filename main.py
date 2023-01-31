import subprocess
import sys
import os
import re

main_file_ext = ''

def build(main_file, output, include_directories, compiler_flags):
    global main_file_ext

    main_file_basename, main_file_ext = os.path.splitext(main_file)
    main_file_basename = os.path.basename(main_file_basename)

    if not output:
        output = main_file_basename

    if main_file_ext == '.c':
        compiler = 'gcc'
    elif main_file_ext == '.cpp':
        compiler = 'g++'
    else:
        print('File is not C or C++ source file!')
        sys.exit(1)

    files = [main_file] + get_included_files_recursive(main_file, include_directories) # Files list contains main file and all dependencies for it
    cmd = [compiler] + compiler_flags + files + ['-o', output]
    for directory in include_directories:
        cmd += ['-I', directory]
    
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e: # Compiler returned error
        print(f'Build failed with return code: {e.returncode}')
        sys.exit(1)
    else:
        print('Build successful!')

def get_included_files_recursive(file, include_directories, visited=[]):
    included_files = []
    with open(file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        match = re.search(r'^\s*#include\s+"(.+)"', line) # Search for include directive
        if not match:
            continue

        included_file = match.group(1) # Getting included file

        for directory in include_directories + [os.path.dirname(file)]:
            included_path = os.path.join(directory, included_file)
            if (not os.path.exists(included_path)) or included_path in visited:
                continue

            visited.append(included_path)

            included_files += get_included_files_recursive(included_path, visited)

            if os.path.splitext(included_path)[1] in ['.h', '.hpp']:
                included_path = included_path.replace('.hpp', main_file_ext).replace('.h', main_file_ext) # If included_path is header, get its source file
            else:
                included_files.append(included_path) # Else, just add it to included_files and go to the next file
                continue
            
            if not os.path.exists(included_path):
                print(f'File {included_path} not found!')
                sys.exit(1)

            included_files += get_included_files_recursive(included_path, visited)
            included_files.append(included_path)

    return included_files

def explain_usage():
    print('Usage: build.py main_file [options]')
    print('Options:')
    print('\t-h --help\t\t\tGet help about usage')
    print('\t-o <output>\t\t\tSet output file name')
    print('\t-I <directory>\t\t\tAdd include directory')
    print('\t--compiler_flags=<flags>\tPass flags directly to the compiler')


if __name__ == '__main__':
    if len(sys.argv) < 2: # Args not passed
        explain_usage()
        sys.exit(1)

    main_file = sys.argv[1]
    output = None
    include_directories = []
    compiler_flags = []

    for i in range(2, len(sys.argv)):
        if sys.argv[i] == '-o':
            if i + 1 >= len(sys.argv):
                print('Option -o requires an argument')
                sys.exit(1)
                
            output = sys.argv[i + 1]
            break

        elif sys.argv[i] == '-I':
            if i + 1 >= len(sys.argv):
                print("Option -I requires an argument")
                sys.exit(1)

            include_directories.append(sys.argv[i + 1])

        elif sys.argv[i].startswith('--compiler_flags='):
            compiler_flags = sys.argv[i].split('=')[1].split(' ')

        elif sys.argv[i] in ['-h', '--help']:
            explain_usage()
            sys.exit(0)

    build(main_file, output, include_directories, compiler_flags)
