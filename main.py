import uuid

import dbjson
import objects

users: dict[uuid.UUID, objects.User] = {}
posts: dict[uuid.UUID, objects.Post] = {}
serialized_objects: dict = {}

def main():
    global users, posts, serialized_objects

    serialized_objects = dbjson.parse_file()

    users = dbjson.get_users(serialized_objects)

    print(users)

    dbjson.save_file(serialized_objects)

if __name__ == "__main__":
    main()