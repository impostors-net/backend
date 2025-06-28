import uuid

import database
import objects

users: dict[uuid.UUID, objects.User] = {}
posts: dict[uuid.UUID, objects.Post] = {}

def main():
    global users, posts

    connection = database.start()
    database.main(connection)

    users = objects.users_from_database(connection)

    connection.close()

if __name__ == "__main__":
    main()