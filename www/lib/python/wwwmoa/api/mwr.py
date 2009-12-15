import sys
import wwwmoa.info.moa

sys.path.append(wwwmoa.info.moa.get_pylib_base())


import moa.info
import moa.dispatcher
import moa.conf


def is_directory_moa(path):
    return moa.info.isMoa(path)

def get_moa_info(path):
    return moa.info.info(path)

def set_moa_parameter(path, key, value):
    moa.conf.setVar(path, key, value)

def get_moa_parameter(path, key):
    job_info=moa.info.info(path)

    job_info_params=job_info["parameters"]

    if key in job_info_params:
        return job_info_params[key]["value"]
    else:
        return ""
