import uuid

import sqlite3

import main
import post

class User:
    def __init__(self, user_uuid: uuid.UUID, user_name: str, password_hash: str):
        self.uuid = user_uuid
        self.name = user_name
        self.password_hash = password_hash

    def get_name(self):
        return self.name

    def get_password_hash(self):
        return self.password_hash

    def get_assigned_posts(self, posts: dict[uuid.UUID, post.Post]) -> dict[uuid.UUID, post.Post]:

        assigned_posts = {}

        for post in posts.values():
            if post.get_owner() == self:
                assigned_posts[post.post_uuid] = post

        return assigned_posts




def from_database(connection: sqlite3.Connection) -> dict[uuid.UUID, User]:
    pass



