import main


def initialize():
    main.initialize()


def signup():
    pass

def basic_auth(username: str, password: str):
    initialize()
    print(username, password)

    print(main.get_users())

    for user in main.get_users().values():
        if user.get_name() == username and user.get_password_hash() == password:
            return {"sub": username}

    return None