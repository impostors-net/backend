import test


def signup():
    pass

def basic_auth(username: str, password: str):
    print(username, password)
    for user in test.user_list:
        if user.get_name() == username and user.get_password_hash() == password:
            return {"sub": username}

    return None