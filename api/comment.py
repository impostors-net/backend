from database import DatabaseManager, User, Post, Comment


def create(context_, body: bytes, uuid: str):
    if body == {}:
        return {"error": "Request body cannot be empty!"}, 400
    manager = DatabaseManager()
    user = context_.get('user', None)
    post = Comment(body.decode("utf-8"), Post.get_by_id(uuid, manager), User.get_by_handle(user, manager))
    return post.get_api_representation(), 200

def fetch(uuid: str):
    manager = DatabaseManager()
    comment = Comment.get_by_id(uuid, manager)
    if comment:
        return comment.get_api_representation(), 200
    else:
        return {"error": "Comment not found"}, 404

def put_vote(uuid: str, body: int, context_):
    if body == {}:
        return {"error": "Request body cannot be empty!"}, 400
    manager = DatabaseManager()
    user = User.get_by_handle(context_.get('user', None), manager)
    comment = Comment.get_by_id(uuid, manager)
    if not comment:
        return { "error": "Comment not found" }, 404
    comment.add_vote(user, body)
    return comment.get_api_representation(), 200

def delete(context_, uuid: str):
    manager = DatabaseManager()
    handle = context_.get('user', None)
    user = User.get_by_handle(handle, manager)
    comment = Comment.get_by_id(uuid, manager)
    if not comment:
        return {"error": "Comment not found"}, 404
    if comment.author.id != user.id:
        return {"error": "You are not the author of this comment"}, 403
    comment.delete()
    return {"message": "Comment deleted successfully"}, 200
