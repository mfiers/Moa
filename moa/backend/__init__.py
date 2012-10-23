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
        pass

    def init(self):
        """
        Initialize this job
        """
        pass
        

    def defineOptions(self, parser):
        """
        Set command line options for this backend
        """
        pass

    def prepare(self):
        pass
    
    def execute(self, command, **options):
        pass
    
