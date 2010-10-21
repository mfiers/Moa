
import os
import time
import twitter

api = twitter.Api(username='__moa__', password='moabird')

def postRun(data):
    api.PostUpdate('Finished %s in %s on %s' % (
        (" ".join(data['args']),
         os.path.basename(data['cwd']),
         time.ctime())))

