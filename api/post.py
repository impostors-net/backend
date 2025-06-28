from database import *


def next_post():
    manager = DatabaseManager()
    post = Post.get_random(manager)
    if not post:
        return {"error": "No posts available"}, 404
    return { "uuid": post.id }, 302, { "Location": f"/post/{post.id}" }

def fetch(uuid):
    manager = DatabaseManager()
    post = Post.get_by_id(uuid, manager)
    if not post:
        return {"error": "Post not found"}, 404
    return post.get_api_representation(), 200

def create(context_, body: str):
    manager = DatabaseManager()
    user = context_.get('user', None)
    post = Post(body, User.get_by_handle(context_, manager))