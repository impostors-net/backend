import hashlib

from database import User, DatabaseManager

def signup(display_name: str, handle: str, password_hash: str):
    password_bytes = password_hash.encode('utf-8')

    # Use SHA-256 hash function to create a hash object
    hash_object = hashlib.sha256(password_bytes)

    # Get the hexadecimal representation of the hash
    actual_password_hash = hash_object.hexdigest()

    manager = DatabaseManager()
    if User.get_by_handle(handle, manager):
        return { "error": "A user with this handle already exists" }, 409
    else:
        user = User(display_name, handle, actual_password_hash, manager)
        return {
            "uuid": user.id,
            "displayName": user.display_name,
            "handle": user.handle
        }, 200
