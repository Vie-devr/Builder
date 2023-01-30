import subprocess
import sys
import os
import utils

def build(main_file, output, compiler_flags):
    main_file_basename, main_file_ext = os.path.splitext(main_file)
    main_file_basename = os.path.basename(main_file_basename)

    files = utils.get_included_files_recursive(main_file) + [main_file]

    if not output:
        output = main_file_basename

    compiler = 'gcc' if main_file_ext == '.c' else 'g++' if main_file_ext == '.cpp' else ''
    if not compiler:
        raise Exception('Wrong file extension!')

    cmd = [compiler] + compiler_flags + files + ['-o', output]
    
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        print(f'Build failed with return code: {e.returncode}')
        sys.exit(1)
    else:
        print('Build successful!')

def explain_usage():
    print('Usage: build.py main_file [options]')
    print('Options:')
    print('\t-h --help\t\t\tGet help about usage')
    print('\t-o <output>\t\t\tSet output file name')
    print('\t--compiler_flags=<flags>\tPass flags directly to the compiler')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        explain_usage()
        sys.exit(1)

    main_file = sys.argv[1]
    output = None
    compiler_flags = []

    for i in range(2, len(sys.argv)):
        if sys.argv[i] == '-o':
            if i + 1 >= len(sys.argv):
                print('Option -o requires an argument')
                sys.exit(1)
                
            output = sys.argv[i + 1]
            break

        elif sys.argv[i].startswith('--compiler_flags='):
            compiler_flags = sys.argv[i].split('=')[1].split(' ')

        elif sys.argv[i] in ['-h', '--help']:
            explain_usage()
            sys.exit(0)

    build(main_file, output, compiler_flags)