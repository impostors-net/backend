from database import DatabaseManager, User

def fetch_by_uuid(uuid):
    manager = DatabaseManager()
    user: User = User.get_by_id(uuid, manager)
    if not user:
        return None, 404
    return user.get_api_representation(), 200
