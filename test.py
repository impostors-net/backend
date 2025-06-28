import uuid

from database import *
from os import remove, path

if path.exists("test.db"):
    remove("test.db")

manager = DatabaseManager("test.db")

users = [
    User("Linus", "libewa", "password", manager),
    User("Paul", "pauljako", "password", manager),
    User("Kleefuchs", "kleefuchs", "password", manager),
    User("Red", "kindasus", "password", manager),
]

post = Post("According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible.", users[0])
post.add_comment("I don't think this is true, bees are actually quite aerodynamic.", users[1])

for post in users[0].get_posts():
    print(post.content)
    for comment in post.get_comments():
        print(comment.content)