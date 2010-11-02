
import moa.logger as l
import moa.backend

class NojobBackend(moa.backend.BaseBackend):
    """
    Nojob backend - placeholde for directories without a job
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
        return False
    
    def execute(self, command):
        """
        Nojob - cannot execute
        """
        l.error("cannot execute 'moa %s'" % command)
        l.error("Maybe try this in a directory containing a moa job?")