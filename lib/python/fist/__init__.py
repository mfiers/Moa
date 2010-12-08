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
    def __init__(self, url, mapPattern=None):
        self.url = url
        if not mapPattern: 
            self.mapPattern = url
        else:
            self.mapPattern = mapPattern
        self.init()
        self.resolved = False

    def init(self):
        self.scheme, self.netloc, self.path, self.glob = \
            self._urlparse(self.url)
            
        self.mapScheme, self.mapNetloc, self.mapPath, self.mapGlob = \
            self._urlparse(self.mapPattern)
        
    def _urlparse(self, url):
        o = urlparse.urlparse(url)
        
        if o.scheme: scheme = o.scheme
        else: scheme = 'file'
        
        netloc = o.netloc
        
        if o.path and o.path[-1] == '/':
            urlpath = o.path[:-1]
            urlglob = '*'
        elif o.path and os.path.isdir(o.path):
            urlpath = o.path
            urlglob = '*'
        elif not o.path:
            urlpath = '*'
            urlglob = '*'
        elif '/' in o.path:
            urlpath, urlglob = o.path.rsplit('/', 1)
        else:
            urlpath='.'
            urlglob=o.path
            
        return scheme, netloc, urlpath, urlglob
    
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
        super(fistFileset, self).init()
        self.resolved = True
        self.extend(self.url)
        
    def resolve(self):
        pass
    

class fistFileset(fistCore):
    """
    Most basic set of files - handle a set of files described by a single URI with wildcards, for
    example::
    
    * `*.txt`
    * `../*.txt`
    * `file:///home/name/data/*.txt`
        
    >>> f = fistFileset('*.txt')
    >>> assert(f.path=='.')
    >>> assert(f.glob=='*.txt')   
    >>> assert(f.path=='.')
    >>> assert(f.glob=='*.txt')     
    >>> f = fistFileset('/tmp')
    >>> assert(f.path=='/tmp')
    >>> assert(f.glob=='*')    
    >>> f = fistFileset('/tmp/*.txt')
    >>> assert(f.path=='/tmp')
    >>> assert(f.glob=='*.txt')       
    >>> f = fistFileset('../*.txt')
    >>> assert(f.path=='..')
    >>> assert(f.glob=='*.txt')        
    >>> f = fistFileset(os.path.join(wd, 'in', '*.txt'))
    >>> f.resolve()
    >>> assert(len(f) == 100)
    >>> f = fistFileset(os.path.join(wd, 'in', 'in1*.txt'))
    >>> f.resolve()
    >>> assert(len(f) == 10)
    >>> f = fistFileset('~/*')
    >>> f.resolve()
    >>> assert(len(f) > 0)
    """
    
    def init(self):
        if '~' in self.url:
            self.url = os.path.expanduser(self.url)
        super(fistFileset, self).init()
    
    def resolve(self):
        self.resolved = True    
        self.extend(glob.glob('%s/%s' % (self.path, self.glob)))

class fistMapset(fistCore):
    """
    fistMapset
    ----------
    
    Map set - map a fileset based on a target uri
    
    >>> f = fistFileset(os.path.join(wd, 'in', 'in*.txt'))
    >>> f.resolve()
    >>> assert(len(f) == 100)
    >>> m = fistMapset('out/test.*.test')
    >>> m.resolve(f)
    
    """
    
    def init(self):
        if '~' in self.url:
            self.url = os.path.expanduser(self.url)
        super(fistMapset, self).init()
    
    def __str__(self):
        return self.url    
    
    def resolver(self, mapFrom, list):
        """
        map all files in the incoming list
        """
##        print 'x' * 80
#        print 'ORIping from %20s -- %20s:' % (mapFrom.mapPath, mapFrom.mapGlob)
#        print 'THIping from %20s -- %20s:' % (mapFrom.path, mapFrom.glob)
#        print 'ORIping to   %20s -- %20s:' % (self.mapPath, self.mapGlob)
#        print 'THIping to   %20s -- %20s:' % (self.path, self.glob)
        reF = ''
        reT = ''
        method = ''
        if '*' in mapFrom.path and '*' in self.path:
            method += 'a'
            #raise Exception("Don't think that this should happen")
            reF = mapFrom.path.replace('*', r'(?P<path>.*)')
            reT = self.path.replace('*', r'\g<path>')
        elif self.path == '*':
            method += 'b'
            reF = r'.*'
            reT = self.path.replace('*', mapFrom.path)
        elif mapFrom.path == '*':
            method += 'c'
            reF = mapFrom.path.replace('*', '.*')
            reT = self.path
        elif ('*' in self.path) or ('*' in mapFrom.path):            
            raise Exception("Cannot handle path globs other than '*'")
        else:
            method += 'd'
            reF = mapFrom.path
            reT = self.path
                      
        if '*' in self.glob and '*' in mapFrom.mapGlob:
            #raise Exception("Don't think that this should happen")
            method += '1'
            reF += '/' + mapFrom.mapGlob.replace('*', r'(?P<glob>[^/]*)')
            reT += '/' + self.mapGlob.replace('*', r'\g<glob>')
        elif '*' in mapFrom.glob:
            method += '2'
            reF += '/' + mapFrom.glob.replace('*', '.*')
            reT += '/' + self.mapGlob        
        else:
            method += '4'
            reF += '/' + mapFrom.mapGlob
            reT += '/' + self.mapGlob

#        print '## method', method
#        print '##### reF', reF
#        print '##### reT', reT
        rex = re.compile(reF)        
        return [rex.sub(reT, x) for x in list]
    
    def resolve(self, mapFrom):
        """
        Resolve the mapped set based on a input fileSet    
        """
        self.extend(self.resolver(mapFrom, mapFrom))
        self.resolved = True                



    
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
 