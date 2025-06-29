import hashlib
from database import User, DatabaseManager
import re

pattern = r'^\w{3,}$'

def signup(display_name: str, handle: str, password_hash: str):
    if not is_valid_handle(handle):
        return { "error": "Handle can only contain word characters and must be at least 3 characters long", "regex": pattern }, 400

    password_bytes = password_hash.encode('utf-8')

    # Use SHA-256 hash function to create a hash object
    hash_object = hashlib.sha256(password_bytes)

    # Get the hexadecimal representation of the hash
    actual_password_hash = hash_object.hexdigest()

    manager = DatabaseManager()
    if User.get_by_handle(handle, manager):
        return { "error": "A user with this handle already exists" }, 409
    else:
        user = User(display_name.replace("<", "&lt;"), handle, actual_password_hash, manager)
        return {
            "uuid": user.id,
            "displayName": user.display_name,
            "handle": user.handle
        }, 200


def is_valid_handle(handle: str):
    return re.match(pattern, handle)