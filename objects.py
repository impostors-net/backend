import uuid

import sqlite3

class User:
    def __init__(self, user_uuid: uuid.UUID, user_name: str, password_hash: str):
        self.uuid = user_uuid
        self.name = user_name
        self.password_hash = password_hash

    def get_name(self):
        return self.name

    def get_password_hash(self):
        return self.password_hash

    def get_assigned_posts(self, posts) -> dict:

        assigned_posts = {}

        for post in posts.values():
            if post.get_owner() == self:
                assigned_posts[post.post_uuid] = post

        return assigned_posts

    def get_assigned_comments(self, comments) -> dict:

        assigned_comments = {}

        for comment in comments.values():
            if comment.get_owner() == self:
                assigned_comments[comment.comment_uuid] = comment

        return assigned_comments

    def __str__(self):
        return self.name

class Post:
    def __init__(self, post_uuid: uuid.UUID, content: str, owner: User, comments: dict):
        self.post_uuid = post_uuid
        self.content = content
        self.owner = owner
        self.comments = comments

    def get_owner(self):
        return self.owner

    def get_content(self):
        return self.content

    def get_comments(self):
        return self.comments

    def add_comment(self, content: str, writer: User):
        comment_uuid = uuid.uuid4()
        self.comments[comment_uuid] = Comment(comment_uuid, content, writer, self)

    def __str__(self):
        return self.content

class Comment:
    def __init__(self, comment_uuid: uuid.UUID, content: str, owner: User, post: Post):
        self.comment_uuid = comment_uuid
        self.content = content
        self.post = post
        self.owner = owner

    def get_post(self):
        return self.post

    def get_owner(self):
        return self.owner

    def get_content(self):
        return self.content

    def __str__(self):
        return self.content


def users_from_database(connection: sqlite3.Connection) -> dict[uuid.UUID, User]:
    pass



