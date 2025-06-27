import uuid

import post
import user

user_list = [user.User(uuid.uuid4(), "linus", "fsdpojfkso"), user.User(uuid.uuid4(), "pauljako", "fsdpojfkso"),
             user.User(uuid.uuid4(), "kleefuchs", "fsdpojfkso"), ]

users: dict[uuid.UUID, user.User] = {}
posts: dict[uuid.UUID, post.Post] = {}

post_list = [post.Post(uuid.uuid4(), "Fancy Post by linus", user_list[0]),
             post.Post(uuid.uuid4(), "Fancy Post by paul", user_list[1])]

for user_obj in user_list:
    users[user_obj.uuid] = user_obj

for post_obj in post_list:
    posts[post_obj.post_uuid] = post_obj

user_list[0].get_assigned_posts(posts)
