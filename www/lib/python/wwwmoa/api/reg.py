## Imports ##

import wwwmoa.info.moa as moainfo
import sys
import os
import os.path
import wwwmoa.env

sys.path.append(moainfo.get_pylib_base())

import moa.api

from wwwmoa.api.regentries import R_JOB, R_DIR, R_FILE, R_WRITE
from wwwmoa.api.regentries import commands as _commands




## Utility Functions ##

def pathSatisfiesRequirements(path, command, method):
    method_dict=_getMethod(command, method)

    if "requirements" in method_dict:
        return _pathSatisfiesRequirements(path, method_dict["requirements"])
    else:
        return _pathSatisfiesRequirements(path, 0)

def _pathSatisfiesRequirements(path, reqs):
    global R_JOB, R_DIR, R_FILE, R_WRITE

    if not os.path.isdir(path) and not os.path.isfile(path):
        return False
    
    if os.path.islink(path):
        return False

    if not os.access(path, os.R_OK | os.W_OK):
        return False

    if _evalReq(R_FILE, reqs) and not os.path.isfile(path):
        return False

    if _evalReq(R_DIR, reqs) and not os.path.isdir(path):
        return False

    if _evalReq(R_WRITE, reqs):
        if wwwmoa.env.is_readonly()==None:
            return False

        if wwwmoa.env.is_readonly():
            return False

    if _evalReq(R_JOB, reqs):
        if not os.path.isdir(path):
            return False

        if not moa.api.isMoaDir(path):
            return False


    return True
    
def isCommandSupported(command):
    try:
        _getCommand(command)
    except NotSupportedError:
        return False

    return True

def isMethodSupported(command, method):
    try:
        _getMethod(command, method)
    except NotSupportedError:
        return False

    return True

def isParameterAccepted(command, method, parameter):
    try:
        _getParameter(command, method, parameter)
    except NotSupportedError:
        return False

    return True

def getSupportedCommands():
    global _commands

    return _commands.keys()

def getSupportedMethods(command):
    return _getCommand(command)["methods"].keys()

def getAcceptedParameters(command, method):
    return _getMethod(command, method)["params"].keys()

def getRequiredParameters(command, method):
    params=getAcceptedParameters(command, method)
    method=_getMethod(command, method)
    required_params=[]

    for p in params:
        if method["params"][p]["mandatory"]:
            required_params.append(p)

    return required_params

def getCommandHelp(command):
    return _getCommand(command)["help"]

def getMethodHelp(command, method):
    return _getMethod(command, method)["help"]

def getParameterHelp(command, method, parameter):
    return _getParameter(command, method, parameter)["help"]

def _evalReq(req, reqs):
    return (req & reqs)==req

def _getCommand(command):
    global _commands

    if command in _commands:
        return _commands[command]
    else:
        raise NotSupportedError

def _getMethod(command, method):
    _command=_getCommand(command)

    if method in _command["methods"]:
        return _command["methods"][method]
    else:
        raise NotSupportedError

def _getParameter(command, method, parameter):
    _method=_getMethod(command, method)

    if parameter in _method["params"]:
        return _method["params"][parameter]
    else:
        raise NotSupportedError




## Custom Exceptions ##

class NotSupportedError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "The command, method, or parameter you specified is not supported."
