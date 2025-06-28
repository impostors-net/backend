import json
import objects
import uuid

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
