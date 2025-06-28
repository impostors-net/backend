import uuid

import dbjson
import objects
import server

users: dict[uuid.UUID, objects.User] = {}
posts: dict[uuid.UUID, objects.Post] = {}
serialized_objects: dict = {}

def main():

    for key, value in dbjson.parse_file().items():
        serialized_objects[key] = value

    for key, value in dbjson.get_users(serialized_objects).items():
        users[key] = value

    print(users)

    for key, value in dbjson.get_posts(serialized_objects, users).items():
        posts[key] = value

    print(posts)

    server.run()

    dbjson.save_file(serialized_objects)

def get_users():
    return users

if __name__ == "__main__":
    main()