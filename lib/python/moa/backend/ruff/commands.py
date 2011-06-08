import os
import re
import glob
from jinja2 import Template as jTemplate

import Yaco

from moa.sysConf import sysConf

class RuffCommands(Yaco.Yaco):
    """
    Read commands for use with Ruff    
    """

    def __init__(self, confDir, moaid):

        super(RuffCommands, self).__init__()
        
        self._confDir = confDir
        self._moaid = moaid
        self.load()
        
    def load(self):
        """
        Load a ruff/jinja file
        """
        templateFile = os.path.join(
            self._confDir, 'template.d',
            '%s.jinja2' % (self._moaid))

        if os.path.exists(templateFile):
            #first, attempt to load 'old style' template files
            with open(templateFile) as F:
                raw = F.read()

            rawc = re.split('###', raw)

            for r in rawc:
                r = r.strip()
                if not r: continue
                splitr = r.split("\n", 1)
                if len(splitr) != 2:                
                    continue

                firstline, rest = splitr

                spl = firstline.strip().split()
                if rest[:2] != '#!':
                    rest = "#!%s\n" % sysConf.default_shell \
                           + rest
                self[spl[0]] = {
                    'script' : rest,
                    'args' : spl[1:] }
            
        # then load new style -looking for files called
        # {{moa_id}}.command.jinja2

        #to be implemented
        glb = "%s/template.d/%s.*.jinja2" % (
            self._confDir, self._moaid)
        for f in glob.glob(glb):
            cname = f.rsplit('/',1)[-1]\
                    .replace('%s.' % self._moaid, '')\
                    .replace('.jinja2', '')
            with open(f) as F:
                raw = F.read()
            self[cname] = {
                'script' : raw,
                'args' : []}
        
            
    def  render(self, command, data):

        if not self.has_key(command):
            return ""

        this = self[command]

        script = this.get('script', '')
        args = this.get('args', [])

        if 'noexpand' in args:
            return script
                
        jt = jTemplate(script)
        rscript = jt.render(data)
        
        if '{{' or '{%' in rscript:
            #try a second level jinja interpretation
            jt2 = jTemplate(rscript)
            rscript = jt2.render(data)

        return rscript
