from database import User, DatabaseManager

def signup(display_name: str, handle: str, password_hash: str):
    manager = DatabaseManager()
    if User.get_by_handle(handle, manager):
        return 409
    else:
        user = User(display_name, handle, password_hash, manager)
        return {
            "uuid": user.id,
            "displayName": user.display_name,
            "handle": user.handle
        }, 200
