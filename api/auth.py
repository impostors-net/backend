def signup():
    pass

def basic_auth(username: str, password: str):
    print(username, password)
    return {"sub": username}