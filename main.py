import database
import user
import server

users: list[user.User] = []

def main():
    global users

    connection = database.start()
    database.main(connection)

    users = user.from_database(connection)

    connection.close()

if __name__ == "__main__":
    main()