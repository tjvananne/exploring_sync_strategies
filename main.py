
# Goal, whenever source.txt is saved, push that data into target.txt
import asyncio
import hashlib
import time # start with time.sleep for now, but try and make this nonblocking async in future
import logging

logging.basicConfig(
    format='[%(asctime)s.%(msecs)03d][%(levelname)s] %(message)s', 
    level=logging.DEBUG, 
    datefmt='%Y-%m-%d %H:%M:%S')


def checksum(filename, hash_factory=hashlib.md5, chunk_num_blocks=8192):
    """
    Hash a file on disk. Read it in in chunks and have the hash factory
    update the hash as we go.

    Question, will this match other md5 hashes the use a different 
    chunk_num_blocks value? Yes. So update creates a "true" hash?
    Actually wait, maybe I can only test this with a low enough
    chunk_num_blocks...

    # https://stackoverflow.com/a/4213255/3586093
    """
    h = hash_factory()
    with open(filename,'rb') as f: 
        for chunk in iter(lambda: f.read(chunk_num_blocks*h.block_size), b''): 
            h.update(chunk)
    return h.digest()



while True:

    if checksum("source.txt") != checksum("target.txt"):
        print("syncing...")
        with open("source.txt", "r") as f_source:
            with open("target.txt", "w") as f_target:
                f_target.truncate()
                f_target.write(f_source.read())

    time.sleep(1)
    print("checking if sync is needed!")
