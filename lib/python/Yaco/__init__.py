"""
"""

import os
import yaml

import moa.utils          

class Yaco(dict):
    """
    Loosely based on http://code.activestate.com/recipes/473786/ (r1)
    
    """
    
    def __init__(self, data={}):
        """
        >>> v= Yaco()
        >>> v.a = 1
        >>> assert(v.a == 1)
        >>> assert(v['a'] == 1)

        >>> v= Yaco({'a':1})
        >>> assert(v.a == 1)
        >>> assert(v['a'] == 1)

        """        
        dict.__init__(self)
        self.update(data)

    def __str__(self):
        """
        >>> v= Yaco({'a':1})
        >>> assert(str(v.a) == '1')
        """
        return str(self.get_data())

    def __setitem__(self, key, value):
        """
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

        """
        
        old_value = super(Yaco, self).get(key, None)
        if isinstance(value, dict):
            #setting a dict
            if isinstance(old_value, Yaco):
                old_value.update(value)
            else:
                super(Yaco, self).__setitem__(key, Yaco(value))
        else:
            super(Yaco, self).__setitem__(key, value)
     
    def __getitem__(self, key):
        """
        >>> v= Yaco()
        >>> v.a = 18       
        >>> assert(v.a == 18)
        >>> assert(isinstance(v.a, int))
        """
        try:
            return super(Yaco, self).__getitem__(key)
        except KeyError:
            rv = Yaco()
            super(Yaco, self).__setitem__(key, rv)
            return rv
        
    def __delitem__(self, name):
        return super(Yaco, self).__delitem__(name)

    def update(self, data):
        """
        
        """
        if not data: return 
        for key, val in data.items():
            if isinstance(val, Yaco):
                raise Exception("Wow - updating with a Yaco - should not happen (%s)!" % val)

            old_value = super(Yaco, self).get(key, None)
            if isinstance(val, dict):
                if old_value and isinstance(old_value, Yaco):
                    old_value.update(val)
                else:
                    super(Yaco, self).__setitem__(key, Yaco(val))
            else:
                super(Yaco, self).__setitem__(key, val)

    __getattr__ = __getitem__
    __setattr__ = __setitem__

    def copy(self):
        ch = Yaco(self)
        return ch
    
    def load(self, from_file):
        """
        Load this dict from_file

        >>> import yaml
        >>> import tempfile
        >>> tf = tempfile.NamedTemporaryFile(delete=False)
        >>> tf.write(yaml.dump({'a' : [1,2,3], 'b': 4, 'c': '5'}))
        
        """
        with open(from_file) as F:
            data = yaml.load(F)
        self.update(data)

    def get_data(self):
        """
        Prepare & parse data for export             
        """
        data = {}
        for k in self.keys():
            if k[0] == '_': continue
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

    import doctest
    doctest.testmod()
