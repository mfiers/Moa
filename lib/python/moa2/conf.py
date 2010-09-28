

import yaml

class Conf:
    def __init__(self, job):

        self.job = job
        self.confDir = os.path.join(job.wd, '.moa')
        
        
