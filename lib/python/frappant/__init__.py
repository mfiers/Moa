"""
frappant
--------

fancy relative paths

Given a directory - this library has code to get to locations relative
to this directory.

For example, given `/tmp/test/data`:
"""

import os
import sys
import fnmatch
import logging

logging.basicConfig(level=logging.WARNING)
lg = logging.getLogger('fapp')

class FrpError(Exception):
    """
    Frp error
    """
    pass

def frp(from_path, fancy):
    """
    Process the from_path given the fancy directory

    >>> if os.path.exists('/tmp/frp'):
    ...    import shutil
    ...    shutil.rmtree('/tmp/frp')
    >>> os.makedirs('/tmp/frp/test/aaa/aaa')
    >>> os.makedirs('/tmp/frp/test/bbb/bbb')
    >>> os.makedirs('/tmp/frp/test/ccc/ccc')
    >>> os.makedirs('/tmp/frp/test/ddd/ddd')
    
    >>> #now for the tests
    >>> base='/tmp/frp/test/ccc/ccc'
    
    >>> assert(frp(base, '..')          == '/tmp/frp/test/ccc' )
    >>> assert(frp(base, '../')         == '/tmp/frp/test/ccc/' )
    >>> assert(frp(base, '../..')       == '/tmp/frp/test' )
    
    >>> assert(frp(base, '../../<<')    == '/tmp/frp/test/aaa' )
    >>> assert(frp(base, '../../<')     == '/tmp/frp/test/bbb' )
    >>> assert(frp(base, '../../>')     == '/tmp/frp/test/ddd' )
    >>> assert(frp(base, '../../>>')    == '/tmp/frp/test/ddd' )
    
    >>> assert(frp(base, '../../</bbb') == '/tmp/frp/test/bbb/bbb' )

    >>> assert(frp(base, '../../a*/')   == '/tmp/frp/test/aaa/' )
    >>> assert(frp(base, '../../>>/?d*')   == '/tmp/frp/test/ddd/ddd' )
    
    """
    ps = from_path.split(os.path.sep)
    fs = fancy.split(os.path.sep)

    if fancy[0] == '/':
        raise FrpError("Absolute paths are not implemented")
        
    current = ps

    for i, element in enumerate(fs):
    
        if i > 0: last_element = fs[i-1]
        else: last_element = ""
            
        lg.debug('processing %d / %s' % (i, element))
        if element == '..':
            if len(current) > 1:
                last_removed = current[-1]
                current = current[:-1]
        elif element in ['<<', '<', '>', '>>']:
            if last_element != "..":
                raise FrpError("Invalid use of <<, <, > or >>")
            current_path = os.path.sep.join(current)
            this_dirlist = [x for x in os.listdir(current_path)
                            if not x[0] == '.']
            this_dirlist.sort()
            pip = this_dirlist.index(last_removed)
            if element == '<<':
                add_to_path = this_dirlist[0]
            elif element == '<':
                add_to_path = this_dirlist[max(0, pip-1)]
            elif element == '>':
                add_to_path = this_dirlist[min(len(this_dirlist)-1,
                                               pip+1)]
            else: #must be >>
                add_to_path = this_dirlist[-1]
            current.append(add_to_path)
        elif ('*' in element) or ('[' in element) or \
               ('?' in element):
            current_path = os.path.sep.join(current)
            hits = []
            for i in os.listdir(current_path):
                if fnmatch.fnmatch(i, element):
                    hits.append(i)
                lg.warning("assessing fnmatch %s" % current_path)
            #hits = fnmatch.fnmatch(current_path)
            if len(hits) > 0:
                hits.sort()
            current.append(hits[0])
        else:
            current.append(element)
            
    return os.path.sep.join(current)
    


if __name__ == "__main__":
    lg.setLevel(logging.DEBUG)
    import doctest
    doctest.testmod()
