from database import DatabaseManager, User


def basic_auth(username, password):
    manager = DatabaseManager()
    user = User.get_by_handle(username, manager)
    if not user or not user.check_password(password):
        print(f"Authentication failed for user: {username}")
        return None
    return {"sub": username}