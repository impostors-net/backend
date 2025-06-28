from database import DatabaseManager, User, Post


def next_post():
    manager = DatabaseManager()
    post = Post.get_random(manager)
    if not post:
        return {"error": "No posts available"}, 404
    return { "uuid": post.id }, 302, { "Location": f"/api/v1/post/{post.id}" }

def fetch(uuid):
    manager = DatabaseManager()
    post = Post.get_by_id(uuid, manager)
    if not post:
        return {"error": "Post not found"}, 404
    return post.get_api_representation(), 200

def create(context_, body: bytes):
    manager = DatabaseManager()
    handle = context_.get('user', None)
    content = body.decode("utf-8")
    user = User.get_by_handle(handle, manager)
    post = Post(content, user)
    return post.get_api_representation(), 200

def delete(context_, uuid: str):
    manager = DatabaseManager()
    handle = context_.get('user', None)
    user = User.get_by_handle(handle, manager)
    post = Post.get_by_id(uuid, manager)
    if not post:
        return {"error": "Post not found"}, 404
    if post.author.id != user.id:
        return {"error": "Forbidden"}, 403
    post.delete()
    return {"message": "Post deleted successfully"}, 200
