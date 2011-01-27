"""
fist
----

**Fi**\ le\ **s**\ e\ **t**\ s

Handle & manipulate sets of files

This module aims at providing classes to handle and manipulate sets of
files. Two simple examples are a simple set containing one file
(:class:`fist.fistSingle`) or a `glob` based set of files
(:class:`fist.fistFileset`). A more complicated example is
:class:`fistMapset` that maps another fileset based on a pattern.

Each fileset inherits from `list` - hence fist filesets behave as
lists.

Future work should allow the definition of remote filesets (for
example over http or ssh).

Each fist class is istantiated with a url defining the file(set). In
the case of :class:`fist.fistFileset` this url contains a globbing
characters::

    fs = fist.fistFileset('/tmp/*,txt')

This fileset object contains a list with all `*.txt` files in
`/tmp`. Subsequently it is possible to map this set

 

"""

import os
import re
import glob
import urlparse

DEBUG=True

if DEBUG:
    import logging
    logging.basicConfig(filename='/tmp/fist.log', level=logging.DEBUG)
    
class fistCore(list):
    """
    Core class for all fist classes
    """
    def __init__(self, url):
        self.url = url
        self.init()
        self.resolved = False

    def init(self):
        self.scheme, self.netloc, self.path, self.glob = \
             self._urlparse(self.url)
            
    def _urlparse(self, url):
        o = urlparse.urlparse(url)
        
        if o.scheme: scheme = o.scheme
        else: scheme = 'file'
        
        netloc = o.netloc

        ext = ''
        
        urlglob = '*'

        if o.path and o.path[-1] == '/':
            urlpath = o.path[:-1]
        elif o.path and os.path.isdir(o.path):
            urlpath = o.path
        elif not o.path:
            urlpath = '*'
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
        super(fistSingle, self).init()
        self.resolved = True
        self.append(self.url)
        
    def resolve(self):
        self.resolved = True
    

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
    
    Map set - map a fileset based on a target uri
    
    >>> f = fistFileset(os.path.join(wd, 'in', '*'))
    >>> f.resolve()
    >>> assert(len(f) == 100)
    >>> ##
    >>> ## Null mapping
    >>> ##
    >>> m = fistMapset('*/*')
    >>> m.resolve(f)
    >>> assert(len(m) == 100)
    >>> assert(os.path.join(wd, 'in/in18.txt') in m)
    >>> ##
    >>> ## simple folder mapping
    >>> ##
    >>> m = fistMapset('out/*')
    >>> m.resolve(f)
    >>> assert(len(m) == 100)
    >>> assert('out/in18.txt' in m)
    >>> ##
    >>> ## simple folder mapping
    >>> ##
    >>> m = fistMapset('./*')
    >>> m.resolve(f)
    >>> assert(len(m) == 100)
    >>> assert('./in18.txt' in m)
    >>> ##
    >>> ## simple folder & mapping & extension append
    >>> ##
    >>> m = fistMapset('out/*.out')
    >>> m.resolve(f)
    >>> assert(len(m) == 100)
    >>> assert('out/in18.txt.out' in m)
    >>> ##
    >>> ## New from fileset - now with a pattern defining the extension
    >>> ##
    >>> f = fistFileset(os.path.join(wd, 'in', '*.txt'))
    >>> f.resolve()
    >>> ##
    >>> ## extension mapping
    >>> ##
    >>> m = fistMapset('out/*.out')
    >>> m.resolve(f)
    >>> assert(len(m) == 100)
    >>> assert('out/in18.out' in m)
    >>> ##
    >>> ## New from fileset - now with a pattern defining file glob &
    >>> ## extension
    >>> ##
    >>> f = fistFileset(os.path.join(wd, 'in', 'in*.txt'))
    >>> f.resolve()
    >>> ##
    >>> ## more complex filename mapping
    >>> ##
    >>> m = fistMapset('out/test*.out')
    >>> m.resolve(f)
    >>> assert(len(m) == 100)
    >>> assert('out/test18.out' in m)
    >>> ##
    >>> ## mapping keeping the extension the same
    >>> ##
    >>> m = fistMapset('out/test*.txt')
    >>> m.resolve(f)
    >>> assert(len(m) == 100)
    >>> assert('out/test18.txt' in m)
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
        
        reF = ''
        reT = ''
        method = ''

        if not '*' in self.path and not '*' in self.glob:
            #special case - no interpretation is needed
            if len(list) == 0:
                return []
            if len(list) == 1:
                return [os.path.join(self.path, self.glob)]
            raise Exception("mapping more than one file to a wildcardless map pattern")

        if '*' in mapFrom.path and '*' in self.path:
            method += 'a'
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
            reF = mapFrom.path.replace('.', '\.')
            reT = self.path
            


        fromStarCount = mapFrom.glob.count('*')
        toStarCount = self.glob.count('*')

        if fromStarCount == 0 and toStarCount == 1:
            method += '9'
            reF += '/(?P<glob>.*)\.[^\.\s]*?$' 
            reT += '/' + self.glob.replace('*', '\g<glob>')
        elif fromStarCount != toStarCount:
            raise Exception("Invalid patterns '%s' -> '%s'" % (mapFrom.glob, self.glob))
        elif  fromStarCount == 0:
            method = '0'
            reF += '/.*$'
            reT += '/' % self.glob
        else:
            addReF = mapFrom.glob
            addReT = self.glob
            for c in range(fromStarCount):
                addReF = addReF.replace('*', '(?P<glob' + str(c) +'>[\S]*)',1)
                addReT = addReT.replace('*', '\g<glob' + str(c) +'>',1)
            reF += '/' + addReF
            reT += '/' + addReT

        if DEBUG:
            logging.info( '#' * 95 )
            logging.info(" Method %s *count %d" % (method, fromStarCount))
            logging.info( 'PATH cur.value : %50s -> %-50s' % (mapFrom.path, self.path))
            logging.info( 'GLOB cur.value : %50s -> %-50s' % (mapFrom.glob, self.glob))
            logging.info( 'REGEX FROM '+ reF)
            logging.info( 'REGEX TO   '+ reT)
            logging.info( 'METHOD %s' % method)
            for x in range(min(len(list),3)):
                logging.info( 'input file no %d: %s' % (x +1, list[x])) 
        rex = re.compile(reF)        
        rv = [rex.sub(reT, x) for x in list]

        if DEBUG:
            for x in range(min(len(list),3)):
                logging.info( 'output file no %d: %s' % (x +1, rv[x])) 
    
        return rv
    
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
 
