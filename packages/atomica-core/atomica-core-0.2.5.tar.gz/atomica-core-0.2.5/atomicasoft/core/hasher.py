"""Utility module providing hashing functionality

Hashing is needed to save up on communication when passing a large file many times while submitting jobs.
This module defines the ``Hasher`` class which provides functionality of packing and unpacking data using hashes.
A hash can be thought of as a unique data fingerprint (SHA256 is used).
Packing is dilling (pickling) data, computing its hash, saving the hash-data pair to a file, and replacing data with its hash.
Unpacking is the reverse functionality: finding the data based on its hash and replacing the hash with the data read from the found file.
``Hasher`` is also included in the package, so can be used as ``atomicasoft.core.Hasher``.

In the example below we assume that ``script`` is a short script with variable content (like a simulation temperature)
whereas ``potential`` is an interatomic potential with lots of data which will be the same for many jobs: ::

    import atomicasoft.core
    class MyLammpsJob:
        def __init__(self, script:str, potential:str):
            self.script = script
            self.potential = atomicasoft.core.Hasher(potential)
        def write_script(self):
            with open('script.in','w') as f:
                f.write(self.script)
        def write_potential(self):
            with open('pot.fs','w') as f:
                f.write(self.potential.data) # note .data, because it is a Hasher()

The ``atomicasoft.jobs`` recursively go through job objects and pack all the ``Hasher()`` objects upon sending jobs
and unpacking upon fetch/receiving jobs or job results.
"""

import dill, hashlib, pathlib, time

from . import serialize

class FetcherIOError(RuntimeError):
    pass

HASH_PATH = pathlib.Path.home() / '.atomica' / '.hashed_objects'
HASH_PATH.mkdir(parents=True, exist_ok=True)
HASH_MAXSIZE = 100 * 1024 * 1024 # default size is 100 MB (safe bound, might want to increase)
HASH_FILE_SIZE_OVERHEAD = 8192

def update_hashdir_size():
    global hashdir_size, hashdir_time
    hashdir_size = 0
    for path in HASH_PATH.iterdir():
        hashdir_size += path.lstat().st_size + HASH_FILE_SIZE_OVERHEAD # effective size
    hashdir_time = HASH_PATH.lstat().st_mtime
update_hashdir_size()

def write_hash(data_hash: str, data_dill: bytes):
    global hashdir_size, hashdir_time
    
    if (HASH_PATH / data_hash).is_file(): return;
    currdir_time = HASH_PATH.lstat().st_mtime
    if(hashdir_time < currdir_time): # need to update
        update_hashdir_size()
    
    # first check if HASH_MAXSIZE would be hit
    if(hashdir_size + HASH_FILE_SIZE_OVERHEAD + len(data_dill) > HASH_MAXSIZE):
        # delete something
        filesize_dict = [(path.lstat().st_mtime, str(path)) for path in HASH_PATH.iterdir()]
        for mtime, filename in sorted(filesize_dict):
            path = pathlib.Path(filename)
            hashdir_size -= HASH_FILE_SIZE_OVERHEAD + path.lstat().st_size
            path.unlink()
            if(hashdir_size + HASH_FILE_SIZE_OVERHEAD + len(data_dill) <= HASH_MAXSIZE):
                break
    with open(HASH_PATH / ('tmp_'+data_hash), 'wb') as f:
        f.write(data_dill)
    (HASH_PATH / ('tmp_'+data_hash)).rename(HASH_PATH / data_hash) # this trick is used to have folder mtime to be the same as the file mtime
    hashdir_time = HASH_PATH.lstat().st_mtime
    hashdir_size += HASH_FILE_SIZE_OVERHEAD + len(data_dill)

# normally the following method will be overriden by atomicasoft.jobs
# to fetch hashes from the database
def fetch_hash(data_hash: str):
    return None

def read_hash(data_hash: str) -> bytes:
    try:
        with open(HASH_PATH / data_hash, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        data_str = fetch_hash(data_hash)
        if data_str is None:
            raise FetcherIOError('unable to fetch hash ' + data_hash)
        return data_str

def is_hash_data_available(data_hash: str) -> bool:
    return (HASH_PATH / data_hash).is_file()

# TODO: safe serialization still packs _data
class Hasher:
    _is_safe_to_serialize = True

    def __init__(self, data, use_safe = False):
        #self._data = data
        self._use_safe = use_safe
        data_str = serialize.dumps(data).encode() if self._use_safe else dill.dumps(data)
        self._hash = hashlib.sha256(data_str).hexdigest()
        write_hash(self._hash, data_str)
        self._data = data

    @staticmethod
    def from_hash(hash, use_safe):
        this = object.__new__(Hasher)
        this._hash = hash;
        this._use_safe = use_safe;
        this._data = serialize.loads(read_hash(hash)) if use_safe else dill.loads(read_hash(hash))
        return this

    def __reduce__(self):
        return (self.from_hash, (self._hash, self._use_safe))

    @property
    def use_safe(self):
        return self._use_safe
    @property
    def hash(self):
        return self._hash
    @property
    def data(self):
        if hasattr(self, '_data'):
            return self._data
        self._data = serialize.loads(read_hash(self._hash)) if self._use_safe else dill.loads(read_hash(self._hash))
        return self._data
    def __eq__(self, other):
        return self._hash == other._hash
    def __hash__(self):
        return hash(self._hash)
    def __repr__(self):
        return f'<Hasher object, hash = {self._hash}>'

#def _deep_pack(obj, obj_set : set, use_safe: bool) -> list:
#    if id(obj) in obj_set:
#        return []
#    obj_set.add(id(obj))
#    hashes = []
#    if isinstance(obj, list):
#        for i in obj:
#            hashes += _deep_pack(i, obj_set, use_safe)
#        return hashes
#    if isinstance(obj, tuple):
#        for i in obj:
#            hashes += _deep_pack(i, obj_set, use_safe)
#        return hashes
#    if isinstance(obj, set):
#        for i in obj:
#            hashes += _deep_pack(i, obj_set, use_safe)
#        return hashes
#    if isinstance(obj, dict):
#        for i in obj:
#            hashes += _deep_pack(obj[i], obj_set, use_safe)
#        return hashes
#    if isinstance(obj, Hasher):
#        return obj.pack(use_safe)
#    if hasattr(obj,'__dict__'):
#        for i in obj.__dict__:
#            hashes += _deep_pack(obj.__dict__[i], obj_set, use_safe)
#        return hashes
#    return []
#def deep_pack(obj, use_safe: bool = False) -> list:
#    return _deep_pack(obj, set(), use_safe)

def _deep_hash_list(obj, obj_set : set) -> list:
    if id(obj) in obj_set:
        return []
    obj_set.add(id(obj))
    hashes = []
    if isinstance(obj, list):
        for i in obj:
            hashes += _deep_hash_list(i, obj_set)
        return hashes
    if isinstance(obj, tuple):
        for i in obj:
            hashes += _deep_hash_list(i, obj_set)
        return hashes
    if isinstance(obj, set):
        for i in obj:
            hashes += _deep_hash_list(i, obj_set)
        return hashes
    if isinstance(obj, dict):
        for i in obj:
            hashes += _deep_hash_list(obj[i], obj_set)
        return hashes
    if isinstance(obj, Hasher):
        return [obj.hash]
    if hasattr(obj,'__dict__'):
        for i in obj.__dict__:
            hashes += _deep_hash_list(obj.__dict__[i], obj_set)
        return hashes
    return []
def deep_hash_list(obj) -> list:
    return _deep_hash_list(obj, set())

#def _deep_unpack(obj, obj_set : set):
#    if id(obj) in obj_set:
#        return 
#    obj_set.add(id(obj))
#    if isinstance(obj, list):
#        for i in obj:
#            _deep_unpack(i, obj_set)
#    if isinstance(obj, tuple):
#        for i in obj:
#            _deep_unpack(i, obj_set)
#    if isinstance(obj, set):
#        for i in obj:
#            _deep_unpack(i, obj_set)
#    if isinstance(obj, dict):
#        for i in obj:
#            _deep_unpack(obj[i], obj_set)
#    if isinstance(obj, Hasher):
#        obj.unpack()
#    if hasattr(obj,'__dict__'):
#        for i in obj.__dict__:
#            _deep_unpack(obj.__dict__[i], obj_set)
#def deep_unpack(obj):
#    _deep_unpack(obj, set())
