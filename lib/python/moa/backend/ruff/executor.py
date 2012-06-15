import os
import stat
import tempfile

import moa.actor

from moa.sysConf import sysConf

def ruffusExecutor(input, output, script, jobData):

    if not sysConf.actor.has_key('files_processed'):
        sysConf.actor.files_processed = []

    sysConf.actor.files_processed.append((input, output))

    wd = jobData['wd']
    tmpdir = os.path.realpath(os.path.abspath(
            os.path.join(wd, '.moa', 'tmp')))
    if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)

    tf = tempfile.NamedTemporaryFile( delete = False,
                                      dir=tmpdir,
                                      prefix='moa',
                                      mode='w')
    
    tf.write(script)
    tf.close()
    os.chmod(tf.name, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

    for k in jobData:
        v = jobData[k]
        if isinstance(v, list):
            os.putenv(k, " ".join(v))
        elif isinstance(v, dict):
            continue
        else:
            os.putenv(k, str(v))

    runner = moa.actor.getRunner()
    rc = runner(jobData['wd'],  [tf.name], jobData, command=jobData['command'])
    if rc != 0:
        raise ruffus.JobSignalledBreak
    #l.debug("Executing %s" % tf.name)
    
