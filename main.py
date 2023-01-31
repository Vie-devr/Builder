import subprocess
import sys
import os
import re

main_file_ext = ''

def build(main_file, output, include_directories, compiler_flags):
    global main_file_ext

    main_file_basename, main_file_ext = os.path.splitext(main_file)
    main_file_basename = os.path.basename(main_file_basename)

    files = [main_file] + get_included_files_recursive(main_file, include_directories) # Files list contains main file and all dependencies for it

    if not output:
        output = main_file_basename

    compiler = 'gcc' if main_file_ext == '.c' else 'g++' if main_file_ext == '.cpp' else '' # What compiler should we use?
    if not compiler:
        raise Exception('File you\'re passed is not C or C++ source file!')

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
    with open(file, 'r') as f: lines = f.readlines()

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

        # included_file_path = os.path.join(os.path.dirname(file), included_file) # And path to it, relative to main.py

        # if included_file_path in visited:
        #     continue

        # visited.append(included_file_path)
        # included_files += [included_file_path] + get_included_files_recursive(included_file_path, visited)

        
        # if os.path.splitext(included_file)[1] in ['.h', '.hpp']: # If file is header
        #     source_file = included_file.replace('.hpp', main_file_ext).replace('.h', main_file_ext) # Getting its source file
        #     source_file_path = os.path.join(os.path.dirname(file), source_file) # And path to it
            
        #     try:
        #         included_files += [source_file_path] + get_included_files_recursive(included_file_path, include_directories, visited)
        #     except:
        #         print(f'File {source_file_path} not found.')
        #         sys.exit(1)
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