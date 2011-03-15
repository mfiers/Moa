"""
Yaco
----

Yaco provides a `dict` like structure that can be serialized to & from
`yaml <http://www.yaml.org/>`_. Yaco objects behave as dictionaries
but also allow attribute access (loosely based on this `recipe <
http://code.activestate.com/recipes/473786/>`_). Sublevel dictionaries
are automatically converted to Yaco objects, allowing sublevel
attribute access, for example::

    >>> x = Yaco()
    >>> x.test = 1
    >>> x.sub.test = 2
    >>> x.sub.test
    2

Note that sub-dictionaries do not need to be initialized. This has as
a consequence that requesting uninitialized items automatically return
an empty Yaco object (inherited from a dictionary).

Yaco can be `found <http://pypi.python.org/pypi/Yaco/0.1.1>`_ in the
`Python package index <http://pypi.python.org/pypi/>`_ and is also
part of the `Moa source distribution
<https://github.com/mfiers/Moa/tree/master/lib/python/Yaco>`_

Autogenerating keys
===================

An important feature (or annoyance) of Yaco is the auto generation of
keys that are not present (yet). For example::

    >>> x = Yaco()
    >>> x.a.b.c.d = 1
    >>> assert(x.a.b.c.d == 1)
    
works - `a`, `b` and `c` are assumed to be `Yaco` dictionaries and d
is give value `1`. This makes populating data structures easy.

It might also generate some confusion when querying for keys in the
Yaco structure - if a key does not exists, it automatically comes back
as an empy `dict` or `Yaco` object (renders as `{}`). This means that
if it is easy to check if a certain 'branch' of a Yaco datastructure
exists::

   >>> x = Yaco()
   >>> assert (not x.a.b)

but now the following works as well:

   >>> assert(x.has_key('a'))
   >>> assert(x.a.has_key('b'))

So, a safe way to test a data structure, without introducing extra
branches is:

   >>> x = Yaco()
   >>> assert(not x.has_key('a'))

Todo: Need to find a more elegant way of testing without introducing
data structures

"""

import os
import sys
import yaml

class Yaco(dict):
    """
    Rather loosely based on http://code.activestate.com/recipes/473786/ (r1)

    >>> v= Yaco()
    >>> v.a = 1
    >>> assert(v.a == 1)
    >>> assert(v['a'] == 1)
    >>> v= Yaco({'a':1})
    >>> assert(v.a == 1)
    >>> assert(v['a'] == 1)
    
    """
    
    def __init__(self, data={}):
        """
        Constructor
        
        :param data: data to initialize the Yaco structure with
        :type data: dict
        """
        dict.__init__(self)
        if type(data) == type("string"):
            data = yaml.load(data)
        self.update(data)

    def __str__(self):
        """
        Map the structure to a string
        
        >>> v= Yaco({'a':1})
        >>> assert(str(v.a) == '1')
        """
        return str(self.get_data())

    def __setattr__(self, key, value):
        """
        Set the value of a key
        
        >>> v= Yaco()
        >>> v.a = 18
        >>> assert(v.a == 18)

        >>> v.a = 72
        >>> assert(v.a == 72)

        >>> v.a = {'b' : 5}
        >>> assert(v.a.b == 5)        

        >>> v.a = {'c' : {'d' : 19}}
        >>> assert(v.a.b == 5)
        >>> assert(v.a.c.d == 19)
        >>> assert(v.a['c'].d == 19)

        >>> #create new instances on the fly
        >>> v.e = 1

        >>> v.f.g = 14
        >>> assert(v.f.g == 14)

        >>> v.f.h.i.j.k.l = 14
        >>> assert(v.f.h.i.j.k.l == 14)

        :param key: The key to set
        :param value: The value to assign to key
        """

        #print "setting %s to %s" % (key, value)
        old_value = super(Yaco, self).get(key, None)
        #sys.stderr.write("\nSetting %s to %s (%s)\n" % (key, value, type(value)))

        if isinstance(value, dict):
            #setting a dict
            if isinstance(old_value, Yaco):
                old_value.update(value)
            elif isinstance(value, Yaco):
                super(Yaco, self).__setitem__(key, value)
            else:
                super(Yaco, self).__setitem__(key, Yaco(value))
        elif isinstance(value, list):
            #parse the list to see if there are dicts - which need to be translated to Yaco objects
            new_value = self._list_parser(value)
            super(Yaco, self).__setitem__(key, new_value)
        else:
            super(Yaco, self).__setitem__(key, value)
     
    def has_key(self, key):
        rv = super(Yaco, self).has_key(key)
        return rv

    def __getattr__(self, key):
        """
        >>> v= Yaco()
        >>> v.a = 18       
        >>> assert(v.a == 18)
        >>> assert(isinstance(v.a, int))
        """
        if key == 'getVersion':
            print self
            print self.__dict__
        try:
            return super(Yaco, self).__getitem__(key)
        except KeyError:
            rv = Yaco()
            super(Yaco, self).__setitem__(key, rv)
            return rv
        
    def __delitem__(self, name):
        return super(Yaco, self).__delitem__(name)

    def _list_parser(self, old_list):
        """
        Recursively parse a list & replace all dicts with Yaco objects
        """
        for i, item in enumerate(old_list):
            if isinstance(item, dict):
                old_list[i] = Yaco(item)
            elif isinstance(item, list):
                old_list[i] = self._list_parser(item)
            else:
                pass
        return old_list

    def update(self, data):
        """
        >>> v = Yaco({'a' : [1,2,3,{'b' : 12}]})
        >>> assert(v.a[3].b == 12)

        >>> v = Yaco({'a' : [1,2,3,[1,{'b' : 12}]]})
        >>> assert(v.a[3][1].b == 12)

        """
        if not data: return 
        for key, value in data.items():
            #if isinstance(value, Yaco):
            #    raise Exception("Wow - updating with a Yaco - "+
            #                    "should not happen (%s = %s)!" % (key, value))

            old_value = super(Yaco, self).get(key, None)
            if isinstance(value, dict):
                if old_value and isinstance(old_value, Yaco):
                    old_value.update(value)
                else:
                    super(Yaco, self).__setitem__(key, Yaco(value))
            elif isinstance(value, list):
                #parse the list to see if there are dicts - which need to be translated to Yaco objects                
                new_value = self._list_parser(value)
                super(Yaco, self).__setitem__(key, new_value)
            else:
                super(Yaco, self).__setitem__(key, value)

    __getitem__ = __getattr__
    __setitem__ = __setattr__

    def copy(self):
        ch = Yaco(self)
        return ch
    
    def load(self, from_file):
        """
        Load this dict from_file

        >>> import yaml
        >>> import tempfile
        >>> tf = tempfile.NamedTemporaryFile(delete=False)
        >>> tf.write(yaml.dump({'a' : [1,2,3, [1,2,3, {'d' : 4}]], 'b': 4, 'c': '5'}))
        >>> tf.close()
        >>> y = Yaco()
        >>> y.load(tf.name)
        >>> assert(y.a[3][3].d == 4)
        """
        from_file = os.path.abspath(os.path.expanduser(from_file))
        with open(from_file) as F:
            data = yaml.load(F)
        self.update(data)

    def get_data(self):
        """
        Prepare & parse data for export

        >>> y = Yaco()
        >>> y.a = 1
        >>> y.b = 2
        >>> y._c = 3
        >>> assert(y._c == 3)
        >>> d = y.get_data()
        >>> assert(d.has_key('a') == True)
        >>> assert(d.has_key('b') == True)
        >>> assert(d.has_key('_c') == False)
        >>> y._private = ['b']
        >>> d = y.get_data()
        >>> assert(d.has_key('a') == True)
        >>> assert(d.has_key('b') == False)
        >>> assert(d.has_key('_c') == False)
        
        """
        data = {}
        _priv = self.get('_private', [])
        for k in self.keys():
            if k in _priv:
                continue
            if k[0] == '_':
                continue
            val = self[k]
            if isinstance(val, Yaco):
                val = val.get_data()
            data[k] = val
        return data
                 
    def save(self, to_file, doNotSave=[]):
        """
        
        """        
        with open(to_file, 'w') as F:
            data = self.get_data()
            for k in data.keys():
                if k in doNotSave:
                    del data[k]
            
            F.write(yaml.dump(data, default_flow_style=False))

if __name__ == "__main__":
    if 'x' in sys.argv:
        y = Yaco()
        y.x.z = 1
        print y.x.z
    else:
        import doctest
        doctest.testmod()
