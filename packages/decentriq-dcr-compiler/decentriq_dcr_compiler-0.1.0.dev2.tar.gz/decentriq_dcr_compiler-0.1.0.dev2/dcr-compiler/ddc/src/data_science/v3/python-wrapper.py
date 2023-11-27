import traceback
import os
import sys
from decentriq_util.error import catch_safe_error


transform_paths = [
    lambda path: path.replace("__main_script.py", "main_script.py")
]


with catch_safe_error(transform_paths):
    sys.path.append("/input")
    import __main_script
