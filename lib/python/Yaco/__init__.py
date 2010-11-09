"""
"""

import os
import yaml

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
                 cardinality = "one",
                 default = None,
                 set_name = None,            
                 ):
        
        self.mandatory = mandatory
        self.cardinality = cardinality
        self.category = category
        self.help = help
        self.value = value
        self.set_name = set_name

        if data_type:
            self.data_type = data_type
        else:
            self.data_type = {
                type("string") : "string",
                type(72.18) : "int",
                type(72) : "float",
                type(True) : "boolean",
                type([]) : "list",
                type(None) : None,
                }[type(self.value)]
        self.allowed = allowed
    
    def check(self):
        dt = self.data_type
        v = self.value
        if dt == 'set' and not v in self.allowed:
            return False
        elif dt == 'string' and type(v) != type("string"):
            return False
        elif dt == 'float' and type(v) != type(72.18):
            return False
        elif dt == 'int' and type(v) != type(72):
            return False
        return True
            
    def set_value(self, v):
        self._value = v
        
    def get_value(self):
        if self._value == None and self.default != None:
            return self.default
        else: 
            return self._value
        
    def del_value(self):
        del self._value
        
    value = property(get_value,set_value,del_value,"Value")
    
    
        
class Yaco(dict):
    """
    Based on http://code.activestate.com/recipes/473786/ (r1)

    """
    
    meta = YacoMeta()
    
    def __init__(self, data={}, set_name=None):
        
        for k in data.keys():
            if type(data[k]) == type({}):
                data[k] = Yaco(data[k], set_name = set_name)
            else:
                data[k] = YacoValue(data[k], set_name = set_name)
                
        dict.__init__(self, data)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, dict.__repr__(self))

    def __setitem__(self, key, value):
        if type(value) == type({}): value = Yaco(value)
        else: value = YacoValue(value)            
        return super(Yaco, self).__setitem__(key, value)

    def __getitem__(self, name):
        return super(Yaco, self).__getitem__(name)
        
    def __delitem__(self, name):
        return super(Yaco, self).__delitem__(name)
       
    def update(self, data, set_name=None):
        
        for k in data.keys():
            if type(data[k]) == type({}): data[k] = Yaco(data[k], set_name=set_name)
            else: data[k] = YacoValue(data[k], set_name=set_name)  
        return super(Yaco, self).update(data)

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
            
    def _get_data(self, set_names=[]):
        """
        Prepare & parse data for export
        """
        data = {}
        for k in self.keys():
            if k[0] == '_': continue
            v = self[k]
                        
            if set_names and \
                isinstance(v, YacoValue) and \
                not v.set_name in set_names:
                continue            
            if isinstance(v, Yaco):
                v = v._get_data(set_names = set_names)
            elif isinstance(v, YacoValue):
                v = v.value
            data[k] = v
        return data
                 
    def save(self, to_file, set_names=[]):
        """
        
        """        
        with open(to_file, 'w') as F:
            F.write(yaml.dump(self._get_data(set_names = set_names), 
                              default_flow_style=False))

if __name__ == "__main__":
    
    import logging as l
    import tempfile
    
    l.basicConfig(level=l.DEBUG)
    
    tmpdir = tempfile.mkdtemp(prefix='Yaco.')
    
    l.info("Start Yaco tests in %s" % tmpdir)
    
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
    y.a.data_type = "int"
    y.a.default = 4
    assert(y.a.check())
    
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
    