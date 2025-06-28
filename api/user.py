import main
from uuid import UUID

import objects


def fetch_by_uuid(uuid, user):

    if UUID(uuid) not in main.get_users():
        return {}, 404

    user_obj: objects.User = main.get_users()[UUID(uuid)]

    response = {
        "data": {
            "uuid": uuid,
            "displayName": user_obj.get_name(),
            "handle": user_obj.get_name()
        },
        "posts": list(user_obj.get_assigned_posts(main.get_posts()).keys())
    }
    return response, 200
