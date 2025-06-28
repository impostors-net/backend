import json
import uuid

import objects

DEFAULT_FILE_PATH = "./database.json"

file_path = DEFAULT_FILE_PATH


def parse_file() -> dict:
    with open(file_path, "rb") as f:
        return json.load(f)


def save_file(serialized_object: dict):
    with open(file_path, "wt") as f:
        json.dump(serialized_object, f)


def get_users(serialized_objects: dict) -> dict[uuid.UUID, objects.User]:
    users = {}

    if "users" not in serialized_objects:
        return {}

    for str_uuid, user in serialized_objects["users"].items():
        users[uuid.UUID(str_uuid)] = objects.User(
            user_uuid=uuid.UUID(str_uuid),
            user_name=user["name"],
            password_hash=user["password"]
        )

    return users


def get_posts(serialized_objects: dict, users: dict[uuid.UUID, objects.User]) -> dict[uuid.UUID, objects.Post]:
    posts = {}

    if "posts" not in serialized_objects:
        return {}

    for str_uuid, post in serialized_objects["posts"].items():
        if uuid.UUID(post["owner"]) not in users:
            continue
        post_owner = users[uuid.UUID(post["owner"])]

        post_roles: dict[objects.User, bool] = {}

        for role_user_uuid, impostor in post["roles"].items():
            if uuid.UUID(role_user_uuid) not in users:
                continue
            role_owner = users[uuid.UUID(role_user_uuid)]

            post_roles[role_owner] = impostor

        post_object = objects.Post(
            post_uuid=uuid.UUID(str_uuid),
            content=post["content"],
            owner=post_owner,
            roles=post_roles,
            comments={}

        )

        for comment_uuid, comment in post["comments"].items():

            if uuid.UUID(comment["owner"]) not in users:
                continue
            comment_writer = users[uuid.UUID(comment["owner"])]

            comment_votes: dict[objects.User, int] = {}

            for vote_owner_uuid, vote_value in comment["votes"].items():
                if uuid.UUID(vote_owner_uuid) not in users:
                    continue
                vote_owner = users[uuid.UUID(vote_owner_uuid)]

                comment_votes[vote_owner] = vote_value

            post_object.add_comment(comment_uuid=uuid.UUID(comment_uuid), content=comment["content"],
                                    writer=comment_writer, votes=comment_votes)

        posts[uuid.UUID(str_uuid)] = post_object

    return posts
