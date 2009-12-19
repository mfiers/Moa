import os.path
import os

## A custom exception class to be used when a Moa implementation is required, but cannot be found.
class MoaNotFoundError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "A Moa implementation was not found."


## Returns the "root" directory for the default Moa implementation.
## Raises a MoaNotFoundError or returns None on failure, depending on the value of raiseerr.
def get_base(raiseerr=False):
    if "MOABASE" in os.environ:
        return os.environ["MOABASE"]
    else:
        if raiseerr:
            raise MoaNotFoundError
        else:
            return None

## Returns the "root" directory for the default Moa implementation library.
## Raises a MoaNotFoundError or returns None on failure, depending on the value of raiseerr.
def get_lib_base(raiseerr=False):
    return os.path.normpath(os.path.join(get_base(raiseerr), "lib"))

## Returns the "root" directory for the default Moa implementation Python library.
## Raises a MoaNotFoundError or returns None on failure, depending on the value of raiseerr.
def get_pylib_base(raiseerr=False):
    return os.path.normpath(os.path.join(get_lib_base(raiseerr),"python"))

## Returns the "var" directory for the default Moa implementation.
## Raises a MoaNotFoundError or returns None on failure, depending on the value of raiseerr.
def get_var_base(raiseerr=False):
    return os.path.normpath(os.path.join(get_base(raiseerr), "var"))

