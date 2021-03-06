# make_hashable.py
#
# Created:  Aug 2015, T. Lukacyzk
# Modified: Feb 2016, T. MacDonald

# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import copy

from arrays import numpy_isloaded, array_type, matrix_type

DictProxyType = type(object.__dict__)

# ----------------------------------------------------------------------
#   Method
# ----------------------------------------------------------------------

def make_hashable(o):
    """ Makes a hashable item from a dictionary, list, tuple or set to any level, that 
        contains only other hashable types (including any lists, tuples, sets, and
        dictionaries).  This allows these types to be used as keys for dictionaries,
        for example.
    
        In the case where other kinds of objects (like classes) need 
        to be hashed, pass in a collection of object attributes that are pertinent. 
    
        For example, a class can be hashed in this fashion:  
            make_hashable([cls.__dict__, cls.__name__])
  
        A function can be hashed like so:
            make_hashable([fn.__dict__, fn.__code__])
      
        original source: http://stackoverflow.com/a/8714242
    """
    
    # already hashable
    if isinstance(o,(int,float,str,set,tuple)):
        return o
    
    # hashing override
    # could pass a next identifier object, which could be passed back to indicate checkout
    if hasattr(o,'make_hashable'):
        return o.make_hashable()
    
    # classes and functions
    if type(o) == DictProxyType:
        o2 = {}
        for k,v in o.items():
            if not k.startswith("__"):
                o2[k] = v
        #: for each item
        o = o2  
    #: if classes
        
    # numpy arrays and matrices
    elif numpy_isloaded and isinstance(o,(array_type,matrix_type)):
        o = o.tolist()
    
    # lists 
    if isinstance(o, list):
        return tuple([make_hashable(e) for e in o])
    
    # dictionaries
    elif isinstance(o,dict):
        new_o = copy.deepcopy(o)
        for k,v in new_o.items():
            new_o[k] = make_hashable(v)
        return tuple(new_o.items())
    
    # unhandled types
    else:
        return o