class BaseBackend(object):
    """
    Base backend class - needs to be overridden!
    """    
    def __init__(self, job):
        """
        Initialize this backend 
        """
        self.job = job
        self.wd = job.wd
        
        
    def isMoa(self):
        """
        Check if the current job is valid according to the 
        backend type
        """
        pass

    def init(self):
        """
        Initialize this job
        """
        pass
        


