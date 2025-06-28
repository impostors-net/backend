from database import *


def create(context_, body: bytes, uuid: str):
    manager = DatabaseManager()
    user = context_.get('user', None)
    post = Comment(body.decode("utf-8"), Post.get_by_id(uuid, manager), User.get_by_handle(user, manager))
    return post.get_api_representation(), 200

def fetch(uuid: str):
    manager = DatabaseManager()
    return Comment.get_by_id(uuid, manager).get_api_representation(), 200

def put_vote(uuid: str, body: int, context_):
    manager = DatabaseManager()
    user = User.get_by_handle(context_.get('user', None), manager)
    comment = Comment.get_by_id(uuid, manager)
    if not comment:
        return None, 404
    comment.add_vote(user, body)
    return comment.get_api_representation(), 200

def delete(context_, uuid: str):
    manager = DatabaseManager()
    handle = context_.get('user', None)
    user = User.get_by_handle(handle, manager)
    comment = Comment.get_by_id(uuid, manager)
    if not comment:
        return {"error": "Post not found"}, 404
    if comment.user.id != user.id:
        return {"error": "Forbidden"}, 403
    comment.delete(manager)
    return {"message": "Comment deleted successfully"}, 200