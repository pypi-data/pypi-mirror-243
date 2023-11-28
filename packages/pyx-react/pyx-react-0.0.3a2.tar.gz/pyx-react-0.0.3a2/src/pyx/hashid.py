
import hashlib

obj_hash_map = {}

def hashID(obj):
    hasher = hashlib.md5()
    input_string = str(id(obj))
    hasher.update(input_string.encode())
    hash_hex = hasher.hexdigest()
    hash_int = int(hash_hex, 16)
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    hash_base62 = ''
    base = len(characters)
    while hash_int > 0:
        hash_int, remainder = divmod(hash_int, base)
        hash_base62 = characters[remainder] + hash_base62
    obj_hash_map[hash_base62] = obj
    return hash_base62

def getObj(obj_hash):
    return obj_hash_map[obj_hash]

# TODO: Track dependancies and remove them when no longer needed
