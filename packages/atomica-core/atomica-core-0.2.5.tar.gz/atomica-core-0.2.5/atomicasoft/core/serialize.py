import json, numpy, copy, base64, re

def b64encode(message):
    return base64.b64encode(message).decode()

def b64decode(message):
    return base64.b64decode(message)

def _id(obj):
    return obj

reduce = {int: _id, float: _id, str: _id, bool: _id, type(None): _id}
recover = {}

# {'l':list, 't': tuple, 's': set, 'd': dict, 'b': bytes}

def reduce_list(obj):
    obj = ['l', copy.copy(obj)]
    return obj
def recover_list(obj):
    return obj
reduce[list] = reduce_list
recover['l'] = recover_list

def reduce_tuple(obj):
    obj = ['t', list(obj)]
    return obj
def recover_tuple(obj):
    return tuple(obj)
reduce[tuple] = reduce_tuple
recover['t'] = recover_tuple

def reduce_set(obj):
    obj = ['s', list(obj)]
    return obj
def recover_set(obj):
    return set(obj)
reduce[set] = reduce_set
recover['s'] = recover_set

def reduce_dict(obj):
    obj = ['d', [[k,v] for k,v in obj.items()]]
    return obj
def recover_dict(obj):
    return dict(obj)
reduce[dict] = reduce_dict
recover['d'] = recover_dict

def reduce_np_array(obj):
    obj = ['np_array', obj.tolist(), {'dtype': obj.dtype.name}]
    return obj
def recover_np_array(obj, dtype):
    return numpy.array(obj, dtype = dtype)
reduce[numpy.ndarray] = reduce_np_array
recover['np_array'] = recover_np_array

def reduce_bytes(obj):
    obj = ['b', [b64encode(obj)]]
    return obj
def recover_bytes(obj):
    return b64decode(obj[0])
reduce[bytes] = reduce_bytes
recover['b'] = recover_bytes

from . import cfg, interfaces, hasher, series
from .interfaces import legacy_mlip2
from .basic import *

def reduce_valerr(obj):
    obj = ['valerr', [obj.val, obj.err]]
    return obj
def recover_valerr(obj):
    return Valerr(obj[0], obj[1])
reduce[Valerr] = reduce_valerr
recover['valerr'] = recover_valerr


module_map = {'atomicasoft.core.cfg': cfg,
              'atomicasoft.core.interfaces.legacy_mlip2': legacy_mlip2,
              'atomicasoft.core.hasher': hasher,
              'atomicasoft.core.series': series,
              }

def reduce_module(obj):
    name = re.search("([^'\\.]*)'>",str(obj.__class__)).group(1)
    is_safe = hasattr(type(obj), '_is_safe_to_serialize') and type(obj)._is_safe_to_serialize
    assert is_safe, f'Error: {obj.__module__}.{name} is not safely serializable'
    obj = [obj.__module__, [name, list(obj.__dict__.items())], {'module':obj.__module__}]
    return obj
def recover_module(dumped_obj, module: str):
    obj_class = getattr(module_map[module], dumped_obj[0])
    is_safe = hasattr(obj_class, '_is_safe_to_serialize') and obj_class._is_safe_to_serialize
    assert is_safe, f'Error: {module}.{dumped_obj[0]} is not safely serializable'
    obj = obj_class.__new__(obj_class)
    obj.__dict__.update(dumped_obj[1])
    return obj

for module_str in module_map:
    reduce[module_str] = reduce_module
    recover[module_str] = recover_module

#def reduce_namespace_obj(obj):
#    name = re.match("<class '([^']*)'>",str(obj.__class__)).group(1)
#    obj = [name, list(obj.__dict__.items())]
#    return obj
#def recover_namespace_obj(dump_obj):
#    obj = cfg.Cfg.__new__(cfg.Cfg)
#    obj.__dict__.update(dump_obj)
#    return obj

def _dump(orig_obj):
    obj = orig_obj
    reduce_func = reduce.get(type(obj))
    if not reduce_func and hasattr(obj,'__module__'):
        reduce_func = reduce.get(obj.__module__)
    if not reduce_func:
        raise ValueError(f'Cannot dump {type(obj)}')
    obj = reduce_func(obj)
    if isinstance(obj, list):
        container = obj[1]
        for i in range(len(container)):
            container[i] = _dump(container[i])
    return obj

def _load(dumped_obj):
    obj = dumped_obj

    if isinstance(obj, list):
        obj = [obj[0], [_load(elem) for elem in obj[1]] ] + obj[2:]
        if len(obj) == 2:
            obj = recover[obj[0]](obj[1])
        elif len(obj) == 3:
            obj = recover[obj[0]](obj[1], **obj[2])
        else: raise ValueError('dumped list should be two or three elements long')

    return obj

def dumps(obj):
    return json.dumps(_dump(obj))

def loads(obj):
    return _load(json.loads(obj))

#["cfg.Cfg",
# [
#     ["tuple",
#      ["cell",
#       ["numpy.ndarray", [["list", [2, 0, 0]], ["list", [0, 2, 0]], ["list", [0, 0, 2]]], {"dtype": "int32"}]]],
#     ["tuple",
#      ["pos",
#       ["numpy.ndarray", [["list", [0.0, 0.0, 0.0]], ["list", [1.0, 1.0, 1.0]]], {"dtype": "float64"}]]],
#     ["tuple",
#      ["types",
#       ["numpy.ndarray", [28, 28], {"dtype": "int32"}]]]]]

#################################################
# old one with dicts:
#def reduce_list(obj):
#    obj = copy.copy(obj)
#    return obj
#def recover_list(obj):
#    return obj
#reduce[list] = reduce_list
#recover['list'] = recover_list
#
#def reduce_set(obj):
#    obj = {'t':'set','d':list(obj)}
#    return obj
#def recover_set(dumped):
#    return set(dumped)
#reduce[set] = reduce_set
#recover['set'] = recover_set
#
#def reduce_tuple(obj):
#    obj = {'t':'tuple','d':list(obj)}
#    return obj
#def recover_tuple(dumped):
#    return tuple(dumped)
#reduce[tuple] = reduce_tuple
#recover['tuple'] = recover_tuple
#
#def reduce_dict(obj):
#    obj = {'t':'dict', 'd': [[k,v] for k,v in obj.items()] }
#    return obj
#def recover_dict(obj):
#    return dict(obj)
#reduce[dict] = reduce_dict
#recover['dict'] = recover_dict
#
#def reduce_np_array(obj):
#    obj = {'t':'numpy.ndarray', 'd':obj.tolist(), 'o':{'dtype': obj.dtype.name}}
#    return obj
#def recover_np_array(obj, dtype):
#    return numpy.array(obj, dtype = dtype)
#reduce[numpy.ndarray] = reduce_np_array
#recover['numpy.ndarray'] = recover_np_array
#
#def reduce_bytes(obj):
#    obj = {'t':'bytes', 'd':[b64encode(obj)]}
#    return obj
#def recover_bytes(obj):
#    return b64decode(obj[0])
#reduce[bytes] = reduce_bytes
#recover['bytes'] = recover_bytes
#
#def dump(orig_obj):
#    obj = orig_obj
#    reduce_func = reduce.get(type(obj))
#    if reduce_func:
#        obj = reduce_func(obj)
#    #elif is_our_namespace(obj):
#    #    obj = reduce_namespace_obj(obj)
#    else: raise ValueError(f'Cannot dump {type(obj)}')
#    if isinstance(obj, list):
#        for i in range(len(obj)):
#            obj[i] = dump(obj[i])
#    elif isinstance(obj, dict):
#        container = obj['d']
#        for i in range(len(container)):
#            container[i] = dump(container[i])
#    return obj
#
#def load(dumped_obj):
#    obj = dumped_obj
#
#    if isinstance(obj, dict):
#        obj['d'] = [load(elem) for elem in obj['d']]
#        opts = obj.get('o',{})
#        obj = recover[obj['t']](obj['d'], **opts)
#
#    return obj
#
#def dumps(obj):
#    return json.dumps(dump(obj))
#
#def loads(obj):
#    return load(json.loads(obj))
