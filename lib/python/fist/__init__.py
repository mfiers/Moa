"""
fist
====

Filesets - 

Handle & manipulate sets of files

"""

import os
import re
import glob
import urlparse

class fistCore(list):
    """
    Core class for all fist classes
    """
    def __init__(self, url):
        self.url = url
        self.init()

    def init(self):
        self._urlparse()
        
    def _urlparse(self):
        o = urlparse.urlparse(self.url)
        
        if o.scheme: self.scheme = o.scheme
        else: self.scheme = 'file'
        
        self.netloc = o.netloc
        
        if o.path and o.path[-1] == '/':
            self.path = o.path[:-1]
            self.glob = '*'
        elif o.path and os.path.isdir(o.path):
            self.path = o.path
            self.glob = '*'
        elif not o.path:
            self.path = '.'
            self.glob = '*'
        elif '/' in o.path:
            self.path, self.glob = o.path.rsplit('/', 1)
        else:
            self.path='.'
            self.glob=o.path
    
    def resolve(self):
        raise Exception("needs to be overridden")    

class fistSingle(fistCore):
    """
    Represents a single file
    
    """
    def init(self):
        """
        Assuming the url is a single file
        """
        self.extend(self.url)
    

class fistFileset(fistCore):
    """
    Most basic set of files - handle a set of files described by a single URI with wildcards, for
    example::
    
    * `*.txt`
    * `../*.txt`
    * `file:///home/name/data/*.txt`
        
    >>> f = fistFileSet('*.txt')
    >>> assert(f.path=='.')
    >>> assert(f.glob=='*.txt')   
    >>> assert(f.path=='.')
    >>> assert(f.glob=='*.txt')     
    >>> f = fistFileSet('/tmp')
    >>> assert(f.path=='/tmp')
    >>> assert(f.glob=='*')    
    >>> f = fistFileSet('/tmp/*.txt')
    >>> assert(f.path=='/tmp')
    >>> assert(f.glob=='*.txt')       
    >>> f = fistFileSet('../*.txt')
    >>> assert(f.path=='..')
    >>> assert(f.glob=='*.txt')        
    >>> f = fistFileSet(os.path.join(wd, 'in', '*.txt'))
    >>> f.resolve()
    >>> assert(len(f) == 100)
    >>> f = fistFileSet(os.path.join(wd, 'in', 'in1*.txt'))
    >>> f.resolve()
    >>> assert(len(f) == 10)
    >>> f = fistFileSet('~/*')
    >>> f.resolve()
    >>> assert(len(f) > 0)
    """
    
    def init(self):
        if '~' in self.url:
            self.url = os.path.expanduser(self.url)
        self._urlparse()
    
    def resolve(self):
        self.extend(glob.glob('%s/%s' % (self.path, self.glob)))

class fistMapset(fistCore):
    """
    fistMapSet
    ----------
    
    Map set - map a fileset based on a target uri
    
    >>> f = fistFileSet(os.path.join(wd, 'in', 'in*.txt'))
    >>> f.resolve()
    >>> assert(len(f) == 100)
    >>> m = fistMapSet('out/test.*.test')
    >>> m.resolve(f)
    >>> m
    
    """
    
    def init(self):
        if '~' in self.url:
            self.url = os.path.expanduser(self.url)
        self._urlparse()
    
    def resolve(self, mapFrom):
        """
        Resolve the mapped set based on a input fileSet
        
        """
        reF = ''
        reT = ''
        if '*' in mapFrom.path and '*' in self.path:
            reF = mapFrom.path.replace('*', r'(.*)')
            reT = self.path.replace('*', r'\1')
        elif '*' in mapFrom.path:
            reF = mapFrom.path.replace('*', '.*')
            reT = self.path
        else:
            reF = mapFrom.path
            reT = self.path
        if '*' in mapFrom.glob and '*' in self.glob:
            reF += '/' + mapFrom.glob.replace('*', r'(.*)')
            reT += '/' + self.glob.replace('*', r'\1')
        elif '*' in mapFrom.glob:
            reF += '/' + mapFrom.glob.replace('*', '.*')
            reT += '/' + self.glob
        else:
            reF += '/' + mapFrom.glob
            reT += '/' + self.glob
            
        rex = re.compile(reF)
        self.extend([rex.sub(reT, x) for x in mapFrom])

    
if __name__ == '__main__':
        
    import tempfile

    wd = tempfile.mkdtemp('.fist')
    indir = os.path.join(wd, 'in')
    outdir = os.path.join(wd, 'out')
    os.mkdir(indir)
    os.mkdir(outdir)

    for x in range(100):
        fn = os.path.join(indir, 'in%02d.txt' % x)
        with open(fn, 'w') as F:
            F.write('x' * 1000)
        fn = os.path.join(outdir, 'out%02d.txt' %x)
        with open(fn, 'w') as F:
            F.write('y' * 1000)
        
    
    import doctest
    doctest.testmod(extraglobs={'wd' : wd})
 