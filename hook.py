# hook.py

import os
import sys
from PyInstaller.utils.hooks import collect_data_files

def hook_init():
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

    # Specify the path to the original database (adjust as needed)
    original_db_path = os.path.join(script_dir, 'CourseInfo.accdb')

    # Collect the database file for PyInstaller
    datas = collect_data_files('', include_py_files=False)
    datas.append((original_db_path, '.'))

    return datas

print(hook_init)