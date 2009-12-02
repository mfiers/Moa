import os.path
import os

## Returns the "root" directory for the default Moa implementation.  Returns None on failure.
def get_base():
    if "MOABASE" in os.environ:
        return os.environ["MOABASE"]
    else:
        return None

## Returns the "root" directory for the default Moa implementation library.  Returns None on failure.
def get_lib_base():
    return os.path.normpath(os.path.join(get_base(), "lib"))

## Returns the "root" directory for the default Moa implementation Python library. Returns None on failure.
def get_pylib_base():
    return os.path.normpath(os.path.join(get_lib_base(),"python"))
