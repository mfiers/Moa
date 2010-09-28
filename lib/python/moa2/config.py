
import os
import yaml
import UserDict
import contextlib

def MAPTYPES = [type(()),type([]),type({})]

# Get a file lock, adapted from:
#  http://code.activestate.com/recipes/576572/
@contextlib.contextmanager
def _fileLock(path, waitDelay=.1, maxWait=100):
    waited = 0
    waitedTooLong = False
    while True:
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_RDWR)
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise
            waited += waitDelay
            time.sleep(waitDelay)
            if waited > maxWait:
                waitedTooLong = True
                break
            else:
                continue
        else:
            break
    if waitedTooLong:
        raise CannotGetAFileLock(path)
    try:
        yield fd
    finally:
        os.unlink(path)


class Config(UserDict.DictMixin):

    def __init__(self, job, autoSave = True):
        self.job = job

        self.configDirLocal = os.path.join(job.wd, '.moa')
        self.configFileLocal = os.path.join(self.configDirLocal, 'config')

        self.configDirUser = os.path.join(job.wd, '.config', 'moa')
        self.configFileUser = os.path.join(self.configDirUser, 'config')

        self.configDirSystem = os.path.join('/etc/', 'moa')
        self.configFileSystem = os.path.join(self.configDirSystem, 'config')

        if os.path.exists(self.configFileLocal):
            with open(self.configFile) as F:
                self.configLocal = yaml.load(F)
        else:
            self.configLocal = {}

        if os.path.exists(self.configFileUser):
            with open(self.configFile) as F:
                self.configUser = yaml.load(F)
        else:
            self.configUser = {}

        if os.path.exists(self.configFileSystem):
            with open(self.configFile) as F:
                self.configSystem = yaml.load(F)
        else:
            self.configSystem = {}

    def save(self):
        self.saveLocal()
        
    def saveLocal(self):
        """
        Save the configuration file
        """
        if not os.path.exists(self.configDirLocal):
            os.makedirs(self.configDirLocal)
        with _fileLock(self.configFileLocal+'.lock'):
            with open(self.configFileLocal) as F:
                yaml.dump(self.configLocal, F)
                                
    # Implement the basic dict functions
    def __getitem__(self, item):

        for d in [self.configLocal,
                  self.configUser,
                  self.configSytem]:
            if item in d:
        if item in self.configLocal:
            rvl = self.configLocal[item]
            if not type(rv) in MAPTYPES:
                return rv
            itemType = type(rv)

        if item in self.configUser:
            rvu = self.configUser[item]
            if not type(rvu) == itemType:
                raise MoaConfigMixedTypes(
                    "Trying to mix %s and %s" % (
                        itemType, type(rvu)))
            
            if not type(rvu) in MAPTYPES:
                return rvu

        if item in self.configSytem:
            rvs = self.configSystem[item]
            if not type(rvs) in MAPTYPES:
                return rvs

        

    def __setitem__(self, item, value):
        if self.configLocal.has_key(item) and \
           self.configLocal[item] == value:
            return
        
        self.configLocal[item] = value
        self.saveLocal()
        
    def keys(self):
        return self.plugins.keys()


    
            
        
