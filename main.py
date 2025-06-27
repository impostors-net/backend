import database
import objects
import server

users: list[objects.User] = []

def main():
    global users

    connection = database.start()
    database.main(connection)

    users = objects.users_from_database(connection)

    connection.close()

if __name__ == "__main__":
    main()