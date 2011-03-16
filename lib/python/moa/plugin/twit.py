# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**twit** - Tweet results
------------------------

Use twitter to send a message upon job completion
"""
import os
import time
import twitter

api = twitter.Api(username='__moa__', password='moabird')

def postRun(data):
    """
    Send a tweet out upon completing the default run
    """
    api.PostUpdate('Finished %s in %s on %s' % (
        (" ".join(data['args']),
         os.path.basename(data['cwd']),
         time.ctime())))

