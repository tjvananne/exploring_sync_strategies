
# Goal, whenever source.txt is saved, push that data into target.txt
import asyncio
import os
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
    chunk_num_blocks... just tested with a very large (100s MB) file
    and it worked properly. This is a true hash.

    # https://stackoverflow.com/a/4213255/3586093
    """
    h = hash_factory()
    with open(filename,'rb') as f: 
        for chunk in iter(lambda: f.read(chunk_num_blocks*h.block_size), b''): 
            h.update(chunk)
    return h.digest()


def get_modified_timestamp(filepath: str) -> float:
    return os.stat(filepath).st_mtime


def file_contents_are_different(filepath1: str, filepath2: str) -> bool:
    """
    Return True if file contents are different.
    Return False if file contents are identical.

    Order of the arguments does not matter.
    """

    return not checksum(filepath1) == checksum(filepath2)


def sync_files(filepath1: str, filepath2: str) -> None:
    """
    Side effect: filepath1 and filepath2 will be synced. This will
    modify the contents of one of these files on disk.

    Order of the arguments does not matter. We'll read from the
    most recently modified file and overwrite the entire contents
    of the less recently modified file.

    TODO: handle conflicts?
    """

    if get_modified_timestamp(filepath1) > get_modified_timestamp(filepath2):
        newer_file = file1
        older_file = file2
        logging.info(f"syncing {filepath1} to {filepath2}")
    else:
        newer_file = file2
        older_file = file1
        logging.info(f"syncing {filepath2} to {filepath1}")

    with open(newer_file, "rb") as f_source:
        with open(older_file, "wb") as f_target:
            f_target.truncate()
            f_target.write(f_source.read())

    return


if __name__ == "__main__":

    while True:

        # Let's make this bidirectional for these two files
        file1 = "source.txt"
        file2 = "target.txt"

        if file_contents_are_different(file1, file2):
            sync_files(file1, file2)

        time.sleep(1)
        # print("checking if sync is needed!")
