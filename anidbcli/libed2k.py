from Crypto.Hash import MD4
import functools
import os
import multiprocessing
from joblib import Parallel, delayed

CHUNK_SIZE = 9728000 # 9500KB
MAX_CORES = 4

def get_ed2k_link(file_path, file_hash=None):
    name = os.path.basename(file_path)
    filesize = os.path.getsize(file_path)
    if file_hash is None:
        md4 = hash_file(file_path)
    else:
        md4 = file_hash
    return "ed2k://|file|%s|%d|%s|" % (name, filesize, md4)

def md4_hash(data):
    m = MD4.new()
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
                # ED2K Quirk:
                # If file size is an exact multiple of the chunk size, 
                # an extra 0-byte chunk MUST be appended and hashed.
                if f.tell() > 0 and f.tell() % CHUNK_SIZE == 0:
                    yield b""
                return 

    with open(file_path, 'rb') as f:
        a = generator(f)
        num_cores = min(multiprocessing.cpu_count(), MAX_CORES)
        
        # prefer="threads" avoids massive memory copying/IPC overhead
        hashes = Parallel(n_jobs=num_cores, prefer="threads")(delayed(md4_hash)(i) for i in a)
        
        # If there's only 1 chunk, the final hash is just the chunk's hash.
        # Otherwise, hash the concatenated chunk hashes.
        if len(hashes) == 1:
            return hashes[0].hex()
        else:
            return md4_hash(b"".join(hashes)).hex()
