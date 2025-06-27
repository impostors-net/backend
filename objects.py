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

    def __str__(self):
        return self.name

class Post:
    def __init__(self, post_uuid: uuid.UUID, content: str, owner: User):
        self.post_uuid = post_uuid
        self.content = content
        self.owner = owner

    def get_owner(self):
        return self.owner

    def get_content(self):
        return self.content

    def __str__(self):
        return self.content


def users_from_database(connection: sqlite3.Connection) -> dict[uuid.UUID, User]:
    pass



