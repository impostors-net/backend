from pycmarkgfm import gfm_to_html
from database import DatabaseManager, User, Post
from flask import request


def random():
    manager = DatabaseManager()
    post = Post.get_random(manager)
    if not post:
        return {"error": "No posts available"}, 404
    return { "uuid": post.id }, 302, { "Location": f"/api/v1/post/{post.id}" }

def list_recent(context_, count: int):
    manager = DatabaseManager()
    posts = Post.get_recent(count, manager)

    handle = context_.get('user', None)

    return [
        post.get_api_representation(User.get_by_handle(handle, manager))
        for post in posts
    ], 200

def fetch(context_, uuid):
    manager = DatabaseManager()
    post = Post.get_by_id(uuid, manager)
    if not post:
        return {"error": "Post not found"}, 404

    handle = context_.get('user', None)

    return post.get_api_representation(User.get_by_handle(handle, manager)), 200

def fetch_html(context_, uuid):
    manager = DatabaseManager()
    post = Post.get_by_id(uuid, manager)
    if not post:
        return {"error": "Post not found"}, 404

    handle = context_.get('user', None)

    return post.get_api_representation(User.get_by_handle(handle, manager), True).content, 200, { "Content-Type": "text/html" }


def create(context_, body: bytes):
    if body == {}:
        return {"error": "Request body cannot be empty!"}, 400
    manager = DatabaseManager()
    handle = context_.get('user', None)
    content = body.decode("utf-8")
    user = User.get_by_handle(handle, manager)
    post = Post(content, user)
    return post.get_api_representation(user), 200

def delete(context_, uuid: str):
    manager = DatabaseManager()
    handle = context_.get('user', None)
    user = User.get_by_handle(handle, manager)
    post = Post.get_by_id(uuid, manager)
    if not post:
        return {"error": "Post not found"}, 404
    if post.author.id != user.id:
        return {"error": "You are not the author of this post"}, 403
    post.delete()
    return {"message": "Post deleted successfully"}, 200
