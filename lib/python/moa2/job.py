


import moa2

class Job:
    """
    An interface for any Moa job
    """

    def __init__(self, wd):
        """
        Constructor.

        Only thing needed here is a directory where the job lives. Moa will try
        to discover if a job has been instantiated.
        
        """
        
        self.wd = wd
        self.config = moa2.Config(self)
    

        
