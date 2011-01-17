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

DEBUG=False

if DEBUG:
    import logging
    logging.basicConfig(filename='/tmp/fist.log', level=logging.DEBUG)
    
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
    >>> m = fistMapset('out/test*.*')
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
            

            
        if '*' in self.glob and '*' in mapFrom.mapGlob:
            #special case - if there the self.glob ends in .*, try to copy the extension 
            #from the fromglob
            if self.glob.count('*') == 2:
                if self.glob[-2:] == '.*' and '.' in mapFrom.mapGlob:
                    method += '1b'
                    reF += '/' + mapFrom.mapGlob.rsplit('.',1)[0].replace('*', r'(?P<glob>[^/]*)')
                    reF += r'\.(?P<ext>[^\.]*)$'                    
                    reT += '/' + self.mapGlob.rsplit('.',1)[0].replace('*', r'\g<glob>')
                    reT += '.' + self.mapGlob.rsplit('.',1)[1].replace('*', r'\g<ext>')
                else:
                    raise Exception('INVALID MAP')
            elif mapFrom.mapGlob.count('*') == 2:
                method += '1c'
                reF += '/' + mapFrom.mapGlob.rsplit('.',1)[0].replace('*', r'(?P<glob>[^/]*)')
                reF += r'\.' + mapFrom.mapGlob.rsplit('.',1)[1].replace('*', r'(?P<ext>[^\.]*)$')
                reT += '/' + self.mapGlob.rsplit('.',1)[0].replace('*', r'\g<glob>')
                reT += '.' + self.mapGlob.rsplit('.',1)[1].replace('*', r'\g<ext>')
            else:
                method += '1a'
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

        if DEBUG:
            logging.info( '#' * 95 )
            logging.info(" Method %s" % method)
            logging.info( 'PATH patterns  : %50s -> %-50s' % (mapFrom.mapPath, self.mapPath))
            logging.info( 'PATH cur.value : %50s -> %-50s' % (mapFrom.path, self.path))
            logging.info( 'GLOB patterns  : %50s -> %-50s' % (mapFrom.mapGlob, self.mapGlob))
            logging.info( 'GLOB cur.value : %50s -> %-50s' % (mapFrom.glob, self.glob))
            logging.info( 'REGEX FROM '+ reF)
            logging.info( 'REGEX TO   '+ reT)
            
        rex = re.compile(reF)        
        rv = [rex.sub(reT, x) for x in list]

        if DEBUG:
            logging.info( '-' * 95)
            logging.info( ' Returning %s' % rv[:3])
    
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
 
