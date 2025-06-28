import uuid

import dbjson
import objects
import server
import pickle

serialized_objects: dict = {}

USERS_PICKLE_FILE = "./users.pkl"
POSTS_PICKLE_FILE = "./posts.pkl"

def main():

    users: dict[uuid.UUID, objects.User] = {}
    posts: dict[uuid.UUID, objects.Post] = {}

    for key, value in dbjson.parse_file().items():
        serialized_objects[key] = value

    for key, value in dbjson.get_users(serialized_objects).items():
        users[key] = value

    print(users)

    set_users(users)

    for key, value in dbjson.get_posts(serialized_objects, users).items():
        posts[key] = value

    print(posts)

    set_posts(posts)

    server.run()

def get_users():
    with open(USERS_PICKLE_FILE, "rb") as f:
        return pickle.load(f)

def set_users(new_users: dict):
    with open(USERS_PICKLE_FILE, "wb") as f:
        pickle.dump(new_users, f)

def get_posts():
    with open(POSTS_PICKLE_FILE, "rb") as f:
        return pickle.load(f)

def set_posts(new_posts: dict):
    with open(POSTS_PICKLE_FILE, "wb") as f:
        pickle.dump(new_posts, f)

if __name__ == "__main__":
    main()
