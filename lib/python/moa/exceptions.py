
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

