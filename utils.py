import os
import re

INCLUDE_PATTERN = r'#include\s*\"(.*)\"'

def get_included_files(file):
    _, file_ext = os.path.splitext(file)

    with open(file, 'r') as f: code = f.read()
    
    included_files = []
    for match in re.findall(INCLUDE_PATTERN, code):
        included_files.append(os.path.join(
            os.path.dirname(file), 
            match.replace('.hpp', file_ext).replace('.h', file_ext)
        ))

    return included_files

def get_included_files_recursive(file, included_files=None):
    if not included_files:
        included_files = []

    for include_file in get_included_files(file):
        if include_file in included_files:
            continue

        included_files.append(include_file)
        get_included_files_recursive(include_file, included_files)

    return included_files