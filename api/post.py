import flask
import random

import main
from uuid import UUID

def next_post():
    post_uuid: UUID = random.choice(list(main.get_posts().keys()))
    return flask.redirect("/api/v1/post/" + str(post_uuid), 302)

def fetch(uuid: str, user):

    if UUID(uuid) not in main.get_posts():
        return {}, 404

    post_object = main.get_posts()[UUID(uuid)]

    api_object = {
        "responseType": "impostor",
        "uuid": post_object.post_uuid,
        "content": post_object.get_content(),
        "user": {
            "uuid": post_object.get_owner().uuid,
            "displayName": post_object.get_owner().get_name(),
            "handle": post_object.get_owner().get_name()
        },
        "comments": [
            "497f6eca-6276-4993-bfeb-53cbbbba6f08"
        ]
    }

    return api_object, 200

def post():
    pass

