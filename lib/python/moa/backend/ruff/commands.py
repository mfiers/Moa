import os
import re
import glob
from jinja2 import Template as jTemplate
import jinja2.exceptions

import Yaco

import moa.ui
from moa.sysConf import sysConf
import moa.logger as l

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
        # {{moa_id}}.command.*

        #to be implemented
        glb = "%s/template.d/%s.*" % (
            self._confDir, self._moaid)

        finare = re.compile(r'.*/' 
                            + self._moaid 
                            + r'\.(\w+)\.(\w+)')

        for f in glob.glob(glb):
            findName = finare.match(f)
            if not findName: 
                #this could be the .jinja or .moa file
                continue
            cname, cext = findName.groups()
            with open(f) as F:
                raw = F.read()
            cargs = []
            if cext != 'jinja':
                cargs.append('noexpand')
            self[cname] = {
                'script' : raw,
                'ext' : cext,
                'args' : cargs}
                    
    def  render(self, command, data):

        if not self.has_key(command):
            return ""

        this = self[command]

        script = this.get('script', '')
        args = this.get('args', [])

        if 'noexpand' in args:
            return script

        if "##moa:noxpand" in script:
            return script
        
        jt = jTemplate(script)

        try:
            rscript = jt.render(data)
        except jinja2.exceptions.UndefinedError:
            l.debug("script")
            l.debug(script)
            raise
            moa.ui.exitError("Error jinja rendering command") 
        
        if '{{' or '{%' in rscript:
            #try a second level jinja interpretation
            jt2 = jTemplate(rscript)
            rscript = jt2.render(data)

        return rscript
