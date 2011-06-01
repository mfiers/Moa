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
from moa.sysConf import sysConf

def postRun(job):
    """
    Send a tweet out upon completing the default run
    """
    #this is a pain :(
    api = twitter.Api(
        consumer_key =  sysConf.plugins.twit.consumer_key,
        consumer_secret =  sysConf.plugins.twit.consumer_secret,
        access_token_key = sysConf.plugins.twit.access_token_key,
        access_token_secret = sysConf.plugins.twit.access_token_secret,
        base_url='http://twitter.com')

    api.PostUpdate('Finished %s in %s on %s' % (
            (" ".join(sysConf.args),
             os.path.basename(sysConf.job.wd),
             time.ctime())))

