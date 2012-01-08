# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 

class InvalidTemplate(Exception):
    pass

class CannotGetAFileLock(Exception):
    """Cannot get a file lock"""
    def __init__(self, f):
        self.d = dir
    def __str__(self):
        return "Cannot get a file lock on %s" % self.f

class NotAMoaDirectory(Exception):
    """This is not a moa directory"""
    def __init__(self, dir):
        self.dir = dir
    def __str__(self):
        return "%s is not a MOA directory" % self.dir

class NotAMoaTemplate(Exception):
    """This is not a valid moa template"""
    def __init__(self, template):
        self.template = template
    def __str__(self):
        return "%s is not a MOA template" % self.template

class MoaFileError(Exception):
    """Error handling a file """
    def __str__(self):
        return "Moa error handling file"

class MoaDirNotWritable(Exception):
    """
    Moa directory is not writable
    """
    def __str__(self):
        return "Moa directory (.moa) is not writable"

class MoaPermissionDenied(Exception):
    """Permission denied - you do not have the rights to perform this opperation """
    def __str__(self):
        return "Permission denied"
