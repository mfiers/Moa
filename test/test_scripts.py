import os
import shutil
import stat
import subprocess as sp
import tempfile
import unittest


class TestScript(unittest.TestCase):

    def __init__(self, script, *args, **kwargs):
        self.script_name = script
        super(TestScript, self).__init__(*args, **kwargs)

        def setUp(self):
            pass

    def runTest(self):

        tmpdir = tempfile.mkdtemp(suffix='moatest')
        tmpfile = os.path.join(tmpdir, 'run.sh')

        shutil.copyfile(self.script_name, tmpfile)
        os.chmod(tmpfile, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        P = sp.Popen(['bash', '-vex', tmpfile],
                     stdout=sp.PIPE, stderr=sp.PIPE,
                     cwd=tmpdir)
        o, e = P.communicate()
        rc = P.returncode
        msg = ""
        if o:
            msg += "STDOUT:\n"
            msg += o.decode('utf-8')
            msg += "\n"
        if e:
            msg += "STDERR:\n"
            msg += e.decode('utf-8')
            msg += "\n"

        self.assertTrue(rc == 0, msg=msg)
        shutil.rmtree(tmpdir)

    def __str__(self):
        return 'TestScript(%s)' % self.script_name


def script_test_suite(subdir):
    test_suite = unittest.TestSuite()
    for script_name in os.listdir(subdir):
        if script_name[-1] == '~':
            continue
        script = os.path.join(subdir, script_name)
        if not os.path.isfile(script):
            continue
        test_suite.addTest(TestScript(script))
    return test_suite


if __name__ == '__main__':
    scriptdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'scripts')
    for subdirname in os.listdir(scriptdir):
        subdir = os.path.join(scriptdir, subdirname)
        suite = script_test_suite(subdir)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
