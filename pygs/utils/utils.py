import hashlib
import json

def hash_string(*args):
    """
    reduces an arbitrary list of strings into a hash
    """
    return hashlib.sha224((json.dumps("".join(args).replace(" ", ""))).encode()).hexdigest()
