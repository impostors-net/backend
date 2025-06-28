from database import DatabaseManager, User

def fetch_by_uuid(uuid):
    manager = DatabaseManager()
    user: User = User.get_by_id(uuid, manager)
    if not user:
        return None, 404
    response = user.get_api_representation()
    response["posts"] = [post.id for post in user.get_posts()]
    return response, 200

def fetch_by_handle(handle):
    manager = DatabaseManager()
    user: User = User.get_by_handle(handle, manager)
    if not user:
        return None, 404
    response = user.get_api_representation()
    response["posts"] = [post.id for post in user.get_posts()]
    return response, 200
