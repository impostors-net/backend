from functools import reduce
import uuid

from database import DatabaseManager, User, Post, Comment, UserRole, Vote

def main():
    manager = DatabaseManager("data.db")

    try:
        user1 = User("Linus", handle="libewa", db_manager=manager)
        user2 = User("Red", handle="kindasus", db_manager=manager)
        user3 = User("Blue", handle="blueberry", db_manager=manager)
    except ValueError:
        user1 = User.get_by_handle("libewa", manager)
        user2 = User.get_by_handle("kindasus", manager)
        user3 = User.get_by_handle("blueberry", manager)

    post = Post(
        "Hello, this is my first post!",
        author=user1
    )

    post.set_user_role(user2, UserRole.IMPOSTOR)
    post.set_user_role(user3, UserRole.INNOCENT)

    comment1 = Comment(
        "Well then, welcome!",
        post=post,
        author=user3,
    )

    comment1.add_vote(user1, Vote.UPVOTE)

    print(f"Post: {post.content} by {post.author.display_name}.")
    print("Comments:")
    for comment in post.get_comments():
        print(f"- {comment.content} by {comment.author.display_name}. {comment.get_votes()}")
    

if __name__ == "__main__":
    main()