
import moa.logger as l
import moa.backend
import moa.ui

def load(job):
    return Nojob(job)

class Nojob(moa.backend.BaseBackend):
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
    
    def execute(self, command, **kwargs):
        """
        Nojob - cannot execute
        """
        moa.ui.fprint("%(red)s%(bold)sNot a moa job%(reset)s")
        moa.ui.fprint("%%(bold)sCannot execute 'moa %s'%%(reset)s" % command)
        moa.ui.fprint("maybe try: 'moa help'")
