import hashlib
import functools
import os
import multiprocessing
from joblib import Parallel, delayed

CHUNK_SIZE = 9728000 # 9500KB
MAX_CORES = 4

def get_ed2k_link(file_path):
    name = os.path.basename(file_path)
    filesize = os.path.getsize(file_path)
    md4 = hash_file(file_path)
    return "ed2k://|file|%s|%d|%s|" % (name,filesize, md4)


def md4_hash(data):
        m = hashlib.new('md4')
        m.update(data)
        return m.digest()

def hash_file(file_path):
    """ Returns the ed2k hash of a given file. """

    

    def generator(f):
        while True:
            x = f.read(CHUNK_SIZE)
            if x:
                yield x
            else:
                return    

    with open(file_path, 'rb') as f:
        a = generator(f)
        num_cores = min(multiprocessing.cpu_count(), MAX_CORES)
        hashes = Parallel(n_jobs=num_cores)(delayed(md4_hash)(i) for i in a)
        if len(hashes) == 1:
            return hashes[0].hex()
        else:
            return md4_hash(b"".join(hashes)).hex()
