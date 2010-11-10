"""
"""

import os
import yaml

import moa.utils

class YacoMeta(dict):
    """A dictionary with attribute-style access. It maps attribute access to
    the real dictionary.  """
    def __init__(self, init={}):
        dict.__init__(self, init)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, dict.__repr__(self))

    def __setitem__(self, key, value):
        return super(YacoMeta, self).__setitem__(key, value)

    def __getitem__(self, name):
        return super(YacoMeta, self).__getitem__(name)

    def __delitem__(self, name):
        return super(YacoMeta, self).__delitem__(name)

    __getattr__ = __getitem__
    __setattr__ = __setitem__
  
    
class YacoValue(object):
    """
    A single value    
    """

    def __init__(self, 
                 value = None,
                 help = None,
                 data_type = None,
                 allowed = [],
                 category = None,
                 mandatory = False,
                 default = None,
                 set_name = None,            
                 ):

        if data_type:
            self._data_type = data_type
        else:
            self._data_type = {
                type("string") : "string",
                type(72.18) : "int",
                type(72) : "float",
                type(True) : "boolean",
                type([]) : "list",
                type(set()) : "set",
                type(None) : None,
                }[type(value)]

        if not value:
            if self._data_type == 'set':
                self.value = set()
            elif self._data_type == 'list': 
                self.value = []
            else:
                self.value = None
        else:
            self.value = value

        self._mandatory = mandatory    
        self._category = category
        self._help = help        
        self._default = default
        self._set_name = set_name  
        self._allowed = allowed

    def update(self, data, set_name=None):
        for k in data.keys():
            if k == 'add':
                self.set_add(data[k])
            if k == 'remove':
                self.set_remove(data[k])
                
    def configure_from(self, data):
        """
        Get item configuration from this the dict data
        """
        self._allowed = data.get('allowed', [])        
        self._category = data.get('category', None)
        self._data_type = data.get('data_type', None)
        self._default = data.get('default', None)
        self._help = data.get('help', None)
        self._mandatory = data.get('mandatory', False) 
        
    def check(self):
        dt = self._data_type
        v = self.value
        if self._allowed and not v in self._allowed:
            return False
        elif dt == 'string' and type(v) != type("string"):
            return False
        elif dt == 'float' and type(v) != type(72.18):
            return False
        elif dt == 'int' and type(v) != type(72):
            return False
        return True
            
    def set_value(self, v):
        if self._data_type == 'set':
            if isinstance(v, set):
                self._value = v
            elif isinstance(v, list):
                self._value = set(v)
            else:
                self._value = set([v])
        elif self._data_type == 'list':
            if isinstance(v, set):
                self._value = list(v)
            elif isinstance(v, list):
                self._value = v
            else:
                self._value = [v]
        else:
            self._value = v
        
    def get_value(self):        
        if self._value == None and self._default != None:
            return self._default
        else: 
            return self._value
        
    def del_value(self):
        del self._value
        
    value = property(get_value,set_value,del_value,"Value")

    def get_add(self):
        raise Exception("cannot call get_add")
    def set_add(self, value):
        if self._data_type == 'set' and isinstance(value, list):
            for i in value:
                self._value.add(i)
    def del_add(self, value):
        raise Exception("cannot call del_add")
    add = property(get_add, set_add, del_add)

    def get_remove(self):
        raise Exception("cannot call get_remove")
    def set_remove(self, value):
        if self._data_type == 'set':
            try:
                self._value.remove(value)
            except KeyError:
                pass           
    def del_remove(self, value):
        raise Exception("cannot call del_remove")
    remove = property(get_remove, set_remove, del_remove)

    def __str__(self):
        return "%s (%s)" % (self._value, self._set_name)

    def __repr__(self):
        return "<Yaco.YacoValue '%s'>" % self._value
        
class Yaco(dict):
    """
    Based on http://code.activestate.com/recipes/473786/ (r1)

    """
    
    def __init__(self, data={}, set_name=None):
        dict.__init__(self)
        self.update(data, set_name=set_name)
        super(Yaco, self).__setitem__('meta', YacoMeta())        

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, dict.__repr__(self))

    def __str__(self):
        return str(self.get_data())

    def __setitem__(self, key, value):
        
        if isinstance(value, dict):
            #setting a dict
            if isinstance(self.get(key), Yaco):
                self[key].update(value)
            else:
                super(Yaco, self).__setitem__(key, Yaco(value))
        else:
            if isinstance(self.get(key), YacoValue):
                self[key].value = value
                self[key]._set_name = None
            else:
                super(Yaco, self).__setitem__(key, YacoValue(value))
        

    def __getitem__(self, name):
        return super(Yaco, self).__getitem__(name)
        
    def __delitem__(self, name):
        return super(Yaco, self).__delitem__(name)

    def update(self, data, set_name=None):
        for key, val in data.items():
            if isinstance(val, YacoValue):
                raise Exception("Wow - updating with a YacoValue - should not happen!")
            if isinstance(val, dict):
                if self.has_key(key):
                    self[key].update(val, set_name=set_name)
                else:
                    super(Yaco, self).__setitem__(
                        key, Yaco(val, set_name=set_name))
            else:
                if self.has_key(key):
                    self[key].value = val
                else:
                    yv = YacoValue(val, set_name = set_name)
                    super(Yaco, self).__setitem__(key, yv)

    __getattr__ = __getitem__
    __setattr__ = __setitem__

    def copy(self):
        ch = Yaco(self)
        return ch
    
    def load(self, from_file, set_name=None):
        """
        Load this dict from_file
        """
        with open(from_file) as F:
            data = yaml.load(F)
        self.update(data, set_name=set_name)

    def keys(self):
        rv = [x for x in super(Yaco, self).keys() if
              (not x[0] == '_') and
              (not x == 'meta')]
        return rv
    
    def get_data(self, set_names=[]):
        """
        Prepare & parse data for export
        """
        data = {}
        for k in self.keys():
            if k == 'meta': continue
            if k[0] == '_': continue
            v = self[k]
                        
            if set_names and \
                isinstance(v, YacoValue) and \
                not v._set_name in set_names:
                continue            
            if isinstance(v, Yaco):
                v = v.get_data(set_names = set_names)
            elif isinstance(v, YacoValue):
                v = v.value
            data[k] = v
        return data
                 
    def save(self, to_file, set_names=[]):
        """
        
        """        
        with open(to_file, 'w') as F:
            F.write(yaml.dump(self.get_data(set_names = set_names), 
                              default_flow_style=False))

if __name__ == "__main__":

    import sys
    import logging as l
    import tempfile
    
    l.basicConfig(level=l.DEBUG)
    
    tmpdir = tempfile.mkdtemp(prefix='Yaco.')
    
    l.info("Start Yaco tests in %s" % tmpdir)


    
    l.info("Start slowly")
    y = Yaco()
    y.a = 1
    y.a._set_name = "set1"
    y.b = 2
    y.b._set_name = "set2"
    y.b = 3
    
    assert( y.get_data(set_names=['set2']) == {})
    assert( y.get_data(set_names=['set2', None]) == {'b' : 3})
    
    #write test yaml
    test_data = { 'type_int' : 72,
                  'type_str' : "string",
                  'sub_dict' : { "sub_var" : 18 },
                }
    
    test_data_2 = { 'other_int' : 18,
                    'other_float' : 5.14,
                    'another_float' : 19.11,
                    'last_int' : 5,
                    'type_str' : "other string",
                  }
    
    test_file = os.path.join(tmpdir, 'test.yaml')
    other_test_file = os.path.join(tmpdir, 'other.test.yaml')
    test_out_file = os.path.join(tmpdir, 'test.out.yaml')
    
    with open(test_file, 'w') as F:
        F.write(yaml.dump(test_data))
    with open(other_test_file, 'w') as F:
        F.write(yaml.dump(test_data_2))
        
    def test_yacco(s):
        assert(s.type_int.value == 72)
        assert(s['type_int'].value == 72)
        assert(s.type_str.value == "string")
        assert(s['type_str'].value == "string")
        assert(s.sub_dict.sub_var.value == 18)
        l.info("success testing")
        
    l.info("test init data")
    y = Yaco(test_data)
    test_yacco(y)
    
    l.info("testing load data")
    y = Yaco()
    y.load(test_file)    
    test_yacco(y)
    
    l.info("init, change and save")
    y = Yaco()
    y.a = 1
    y.b = "b"
    y.c = {}
    y.c.a = 3
    y.save(test_out_file)
    with open(test_out_file) as F:
        y = yaml.load(F)
    #note: this is just a dict (with dicts) NOT a Yaco object
    assert(y['a'] == 1)
    assert(y['c']['a'] == 3)

    l.info("type checking")
    y = Yaco()
    y.a = 1
    y.a._data_type = "int"
    y.a._default = 4
    assert(y.a.check())

    y.a = "string"
    assert(y.a.check() == False)

    y.a = 4
    assert(y.a.check())

    l.info("sets")
    y = Yaco()
    y.a = set()
    y.a = [1,2,3]
    y.a.add = 4
    assert(y.a.value == set([1,2,3,4]))
    y.a.remove = 3
    assert(y.a.value == set([1,2,4]))
    
    l.info("Multiple config files")
    y = Yaco()
    y.load(test_file, set_name='set1')
    y.load(other_test_file, set_name='set2')
    y.rabbit = "Oryctolagus cuniculus"

    l.info(" testing save set2")
    y.save(test_out_file, set_names=['set2'])
    #load yaml
    with open(test_out_file) as F:
        z = yaml.load(F)
        
    assert(z.has_key("rabbit") == False)
    assert(z.has_key("type_int") == False)
    assert(z['type_str'] == "other string")
    assert(z['other_int'] == 18)
    assert(z['other_float'] == 5.14)
    
    l.info(" testing save set2 & new fields")
    y.save(test_out_file, set_names=['set2', None])
        #load yaml
    with open(test_out_file) as F:
        z = yaml.load(F)
    assert(z['rabbit'] == "Oryctolagus cuniculus")
    assert(z['last_int'] == 5)
    assert(z['type_str'] == "other string")
    
    l.info(" testing save set1")
    y.save(test_out_file, set_names=['set1'])
        #load yaml
    with open(test_out_file) as F:
        z = yaml.load(F)
    assert(z.has_key("rabbit") == False)
    assert(z["type_int"] == 72)
    assert(z.has_key("type_str") == False)
    
