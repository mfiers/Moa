"""
"""

import os
import yaml

import moa.utils  

class YacoInvalidSet(Exception):
    pass

class YacoValue(object):
    """
    A single value

    >>> v = YacoValue(value = 1)
    >>> assert(v.value == 1)    
    >>> v = YacoValue(value = 'string')
    >>> assert(v.value == 'string')
    
    """
    def __init__(self, value = None):
        """

        >>> v = YacoValue(value=1)
        >>> assert(v.value == 1)
        >>> v = YacoValue()
        >>> assert(v.value == None)
        """
        self._value = value

    def __setattr__(self, key, value):
        if key == 'value':            
            return super(YacoValue, self).__setattr__('_value', value)
        if key[0] == '_':
            return super(YacoValue, self).__setattr__(key, value)
        else:
            raise YacoInvalidSet()

    def set_value(self, v):
        """
        >>> v = YacoValue()
        >>> assert(v.value == None)
        >>> v.value = 1
        >>> assert(v.value == 1)        
        """
        self._value = v
        
    def get_value(self):
        """
        >>> v = YacoValue(value = 1)
        >>> assert(v.value == 1)
        """
        return self._value
        
    def del_value(self):
        """
        >>> v = YacoValue(value = 1)
        >>> assert(v.value == 1)        
        >>> del(v.value)
        >>> assert(v.value == None)
        """
        self._value = None
        
    value = property(get_value,set_value,del_value,"Value")

    def __str__(self):
        """
        >>> v = YacoValue(value = 1)
        >>> assert(str(v) ==  '1')        
        """
        return str(self._value)

        

class Yaco(dict):
    """
    Based on http://code.activestate.com/recipes/473786/ (r1)
    
    """
    
    def __init__(self, data={}):
        """
        >>> v= Yaco()
        >>> v.a = 1
        >>> assert(v.a.value == 1)
        >>> assert(v['a'].value == 1)

        >>> v= Yaco({'a':1})
        >>> assert(v.a.value == 1)
        >>> assert(v['a'].value == 1)

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
        >>> assert(v.a.value == 18)

        >>> v.a = 72
        >>> assert(v.a.value == 72)

        >>> v.a = {'b' : 5}
        >>> assert(v.a.b.value == 5)        

        >>> v.a = {'c' : {'d' : 19}}
        >>> assert(v.a.b.value == 5)
        >>> assert(v.a.c.d.value == 19)
        >>> assert(v.a['c'].d.value == 19)

        >>> #create new instances on the fly
        >>> v.e = 1

        >>> v.f.g = 14
        >>> assert(v.f.g.value == 14)

        >>> v.f.h.i.j.k.l = 14
        >>> assert(v.f.h.i.j.k.l.value == 14)

        """
        
        old_value = super(Yaco, self).get(key, None)        
        if isinstance(value, dict):
            #setting a dict
            if isinstance(old_value, Yaco):
                old_value.update(value)
            else:
                super(Yaco, self).__setitem__(key, Yaco(value))
        else:
            if isinstance(old_value, YacoValue):
                old_value.value = value
            else:
                super(Yaco, self).__setitem__(key, YacoValue(value))
     
    def __getitem__(self, key):
        """
        >>> v= Yaco()
        >>> v.a = 18       
        >>> assert(v.a.value == 18)
        >>> assert(isinstance(v.a, YacoValue))
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
        for key, val in data.items():
            if isinstance(val, YacoValue) or isinstance(val, Yaco):
                raise Exception("Wow - updating with a Yaco(Value) - should not happen!")

            old_value = super(Yaco, self).get(key, None)
            if isinstance(val, dict):
                if old_value and isinstance(old_value, Yaco):
                    old_value.update(val)
                else:
                    super(Yaco, self).__setitem__(key, Yaco(val))
            else:
                if old_value and isinstance(old_value, YacoValue):
                    old_value.value = val
                else:
                    super(Yaco, self).__setitem__(key, YacoValue(val))

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
            elif isinstance(val, YacoValue):                
                val = val._value
                if val == None: continue
            else:
                raise Exception('Should not have naked values in a Yaco structure')
            data[k] = val
        return data
                 
    def save(self, to_file):
        """
        
        """        
        with open(to_file, 'w') as F:
            data = self.get_data()
            F.write(yaml.dump(data, default_flow_style=False))

if __name__ == "__main__":

    import doctest
    doctest.testmod()
