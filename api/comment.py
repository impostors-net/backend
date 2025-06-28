from uuid import UUID

import main
import objects


def put_vote():
    pass

def fetch(uuid, user):
    posts = main.get_posts()

    comment_obj: objects.Comment = None

    for post in posts.values():
        for comment in post.get_comments().values():
            if comment.comment_uuid == UUID(uuid):
                comment_obj = comment

    if comment_obj is None:
        return {}, 404

    authed_user_obj: objects.User = None

    for user_obj in main.get_users().values():
        if user_obj.get_name() == user:
            authed_user_obj = user_obj

    response = {
        "uuid": uuid,
        "content": comment_obj.get_content(),
        "post": comment_obj.get_post().post_uuid,
        "user": {
            "uuid": comment_obj.get_owner().uuid,
            "displayName": comment_obj.get_owner().get_name(),
            "handle": comment_obj.get_owner().get_name()
        },
        "score": comment_obj.get_score(),
        "yourVote": 0
    }

    print(comment_obj.get_votes().keys())

    for vote_user_obj in comment_obj.get_votes().keys():
        if vote_user_obj.uuid == authed_user_obj.uuid:
            response["yourVote"] = comment_obj.get_votes()[vote_user_obj]

    return response, 200


def create():
    pass
