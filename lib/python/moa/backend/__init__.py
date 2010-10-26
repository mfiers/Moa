class BaseBackend(object):
    """
    Base backend class - needs to be overridden!
    """    
    def __init__(self, job):
        """
        Initialize this backend 
        """
        self.job = job
        
        
    def isMoa(self):
        """
        Check if the current job is valid according to the 
        backend type
        """
        
        


