import hashlib
import functools
import os

CHUNK_SIZE = 9728000 # 9500KB

def get_ed2k_link(file_path):
    name = os.path.basename(file_path)
    filesize = os.path.getsize(file_path)
    md4 = hash_file(file_path)
    return "ed2k://|file|%s|%d|%s|" % (name,filesize, md4)



def hash_file(file_path):
    """ Returns the ed2k hash of a given file. """

    md4 = hashlib.new('md4').copy

    def generator(f):
        while True:
            x = f.read(CHUNK_SIZE)
            if x:
                yield x
            else:
                return

    def md4_hash(data):
        m = md4()
        m.update(data)
        return m.digest()

    with open(file_path, 'rb') as f:
        a = generator(f)
        hashes = [md4_hash(data) for data in a]
        if len(hashes) == 1:
            return hashes[0].encode("hex")
        else:
            return md4_hash(b"".join(hashes)).hex()
