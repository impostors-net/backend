import uuid

import objects

user_list = [objects.User(uuid.uuid4(), "linus", "fsdpojfkso"), objects.User(uuid.uuid4(), "pauljako", "fsdpojfkso"),
             objects.User(uuid.uuid4(), "kleefuchs", "fsdpojfkso"), ]

users: dict[uuid.UUID, objects.User] = {}
posts: dict[uuid.UUID, objects.Post] = {}

post_list = [objects.Post(uuid.uuid4(), "Fancy Post by linus", user_list[0], {}, {}),
             objects.Post(uuid.uuid4(), "Fancy Post by paul", user_list[1], {}, {})]

for user_obj in user_list:
    users[user_obj.uuid] = user_obj

for post_obj in post_list:
    posts[post_obj.post_uuid] = post_obj

post_list[0].add_comment("Comment by paul", user_list[1], {})
post_list[0].add_comment("Comment by kleefuchs", user_list[2], {})

for post in user_list[0].get_assigned_posts(posts).values():
    print(post)
    for comment in post.get_comments().values():
        print(comment)


for comment in user_list[2].get_assigned_comments(post_list[0].get_comments()).values():
    print(comment)