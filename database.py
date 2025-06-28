import hashlib
import random
import sqlite3
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

class UserRole(Enum):
    IMPOSTOR = True
    INNOCENT = False

class ResponseType(Enum):
    IMPOSTOR = "impostor"
    INNOCENT = "innocent"
    AUTHOR = "author"


class Vote(Enum):
    UPVOTE = 1
    NONE = 0
    DOWNVOTE = -1

class DatabaseManager:
    def __init__(self, db_path: str = "./data/data.sqlite"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                display_name TEXT NOT NULL,
                handle TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        
        # Posts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                author_id TEXT NOT NULL,
                FOREIGN KEY (author_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        
        # Comments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                post_id TEXT NOT NULL,
                author_id TEXT NOT NULL,
                FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE,
                FOREIGN KEY (author_id) REFERENCES users (id)
            )
        ''')
        
        # Post roles table (many-to-many relationship)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS post_roles (
                post_id TEXT,
                user_id TEXT,
                role INTEGER,
                PRIMARY KEY (post_id, user_id),
                FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        
        # Comment votes table (many-to-many relationship)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comment_votes (
                comment_id TEXT,
                user_id TEXT,
                vote INTEGER,
                PRIMARY KEY (comment_id, user_id),
                FOREIGN KEY (comment_id) REFERENCES comments (id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        conn.close()

class User:
    def get_api_representation(self) -> Dict[str, str]:
        return {
            "uuid": self.id,
            "displayName": self.display_name,
            "handle": self.handle
        }

    def __init__(self, display_name: str, handle: str, password_hash: str, db_manager: DatabaseManager):
        existing = User.get_by_handle(handle, db_manager)
        if existing:
            self.id = existing.id
            self.display_name = existing.display_name
            self.handle = existing.handle
            self.password_hash = existing.password_hash
            self.db_manager = db_manager
        else:
            self.id = str(uuid.uuid4())
            self.display_name = display_name
            self.handle = handle
            self.password_hash = password_hash
            self.db_manager = db_manager
            self._save()
    
    def _save(self):
        """Save user to database"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (id, display_name, handle, password_hash) VALUES (?, ?, ?, ?)",
            (self.id, self.display_name, self.handle, self.password_hash)
        )
        conn.commit()
        conn.close()
    
    @classmethod
    def get_by_id(cls, user_id: str, db_manager: DatabaseManager) -> Optional['User']:
        """Retrieve user by ID"""
        conn = sqlite3.connect(db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT display_name, handle, password_hash FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            user = cls.__new__(cls)
            user.id = user_id
            user.display_name = result[0]
            user.handle = result[1]
            user.password_hash = result[2]
            user.db_manager = db_manager
            return user
        return None

    @classmethod
    def get_by_handle(cls, handle: str, db_manager: DatabaseManager) -> Optional['User']:
        """Retrieve user by handle"""
        conn = sqlite3.connect(db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, display_name, password_hash FROM users WHERE handle = ?", (str(handle),))
        result = cursor.fetchone()
        conn.close()
        if result:
            user = cls.__new__(cls)
            user.id = result[0]
            user.display_name = result[1]
            user.handle = handle
            user.password_hash = result[2]
            user.db_manager = db_manager
            return user
        else:
            return None
    
    def get_posts(self) -> List['Post']:
        """Get all posts by this user"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM posts WHERE author_id = ?", (self.id,))
        post_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return [Post.get_by_id(post_id, self.db_manager) for post_id in post_ids]


    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the stored hash"""
        password_bytes = password.encode('utf-8')

        # Use SHA-256 hash function to create a hash object
        hash_object = hashlib.sha256(password_bytes)

        # Get the hexadecimal representation of the hash
        other_password_hash = hash_object.hexdigest()

        return self.password_hash == other_password_hash
    
    def get_comments(self) -> List['Comment']:
        """Get all comments by this user"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM comments WHERE author_id = ?", (self.id,))
        comment_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return [Comment.get_by_id(comment_id, self.db_manager) for comment_id in comment_ids]

class Post:
    def get_api_representation(self, user: User) -> Dict[str, str]:

        response_type = self.get_response_type(user)

        response = {
            "uuid": self.id,
            "content": "You are the impostor!" if response_type == ResponseType.IMPOSTOR else self.content,
            "author": self.author.get_api_representation(),
            "createdAt": self.created_at,
            "response_type": response_type.value,
            "comments": [comment.id for comment in self.get_comments()],
            "competitionFinished": self.competition_finished(),
        }
        return response

    def __init__(self, content: str, author: User):
        self.id = str(uuid.uuid4())
        self.content = content
        self.created_at = datetime.now().isoformat()
        self.author = author
        self.db_manager = author.db_manager
        self._save()

    def get_response_type(self, user: User) -> ResponseType:
        if user.id == self.author.id:
            return ResponseType.AUTHOR

        existing_roles = self.get_user_roles()

        if user.id in existing_roles:
            is_impostor = existing_roles[user.id].value

        else:
            is_impostor = random.random() < 0.1
            role = UserRole(bool(is_impostor))
            self.set_user_role(user, role)

        if is_impostor:
            role_string = ResponseType.IMPOSTOR
        else:
            role_string = ResponseType.INNOCENT
        return role_string
    
    def _save(self):
        """Save post to database"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO posts (id, content, created_at, author_id) VALUES (?, ?, ?, ?)",
            (self.id, self.content, self.created_at, self.author.id)
        )
        conn.commit()
        conn.close()
    
    @classmethod
    def get_by_id(cls, post_id: str, db_manager: DatabaseManager) -> Optional['Post']:
        """Retrieve post by ID"""
        conn = sqlite3.connect(db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT content, created_at, author_id FROM posts WHERE id = ?", (post_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            post = cls.__new__(cls)
            post.id = post_id
            post.content = result[0]
            post.created_at = result[1]
            post.author = User.get_by_id(result[2], db_manager)
            post.db_manager = db_manager
            return post
        return None
    
    @classmethod
    def get_random(cls, db_manager: DatabaseManager) -> Optional['Post']:
        """Retrieve a random post"""
        conn = sqlite3.connect(db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM posts ORDER BY RANDOM() LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return cls.get_by_id(result[0], db_manager)
        return None

    @classmethod
    def get_recent(cls, limit: int, db_manager: DatabaseManager) -> List['Post']:
        """Retrieve a list of posts with a limit"""
        conn = sqlite3.connect(db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM posts ORDER BY created_at DESC LIMIT ?", (limit,))
        post_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return [cls.get_by_id(post_id, db_manager) for post_id in post_ids if post_id is not None]
    
    def get_comments(self) -> List['Comment']:
        """Get all comments for this post"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM comments WHERE post_id = ?", (self.id,))
        comment_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return [Comment.get_by_id(comment_id, self.db_manager) for comment_id in comment_ids]

    def add_comment(self, content: str, author: User) -> "Comment":
        """Add a comment to this post"""
        comment = Comment(content, self, author)
        return comment
    
    def set_user_role(self, user: User, role: UserRole):
        """Set role for a user in this post"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO post_roles (post_id, user_id, role) VALUES (?, ?, ?)",
            (self.id, user.id, role.value)
        )
        conn.commit()
        conn.close()
    
    def get_user_roles(self) -> Dict[str, UserRole]:
        """Get all user roles for this post"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, role FROM post_roles WHERE post_id = ?", (self.id,))
        roles = {user_id: UserRole(bool(role)) for user_id, role in cursor.fetchall()}
        conn.close()
        return roles

    def competition_finished(self) -> bool:
        """Check if the competition for this post has finished"""
        # This is a placeholder implementation. You can implement your own logic.
        # For example, you might check if the post was created more than 24 hours ago.
        created_at = datetime.fromisoformat(self.created_at)
        return (datetime.now() - created_at).total_seconds() > 60*60*24*3 # 3 days
    
    def delete(self):
        """Delete this post from the database"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM posts WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()
        
        # delete related comments and votes
        Comment.delete_by_post_id(self.id, self.db_manager)

class Comment:
    def get_api_representation(self) -> Dict[str, str]:
        return {
            "uuid": self.id,
            "content": self.content,
            "author": self.author.get_api_representation(),
            "post": self.post.id,
            "createdAt": self.created_at,
            "score": sum(vote.value for vote in self.get_votes().values()),
            "isImpostor": self.is_impostor(self.author),
            "yourVote": self.get_votes().get(self.author.id, Vote.NONE).value
        }

    def __init__(self, content: str, post: Post, author: User):
        self.id = str(uuid.uuid4())
        self.content = content
        self.created_at = datetime.now().isoformat()
        self.post = post
        self.author = author
        self.db_manager = post.db_manager
        self._save()
    
    def _save(self):
        """Save comment to database"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO comments (id, content, created_at, post_id, author_id) VALUES (?, ?, ?, ?, ?)",
            (self.id, self.content, self.created_at, self.post.id, self.author.id)
        )
        conn.commit()
        conn.close()
    
    @classmethod
    def get_by_id(cls, comment_id: str, db_manager: DatabaseManager) -> Optional['Comment']:
        """Retrieve comment by ID"""
        conn = sqlite3.connect(db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT content, created_at, post_id, author_id FROM comments WHERE id = ?", (comment_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            comment = cls.__new__(cls)
            comment.id = comment_id
            comment.content = result[0]
            comment.created_at = result[1]
            comment.post = Post.get_by_id(result[2], db_manager)
            comment.author = User.get_by_id(result[3], db_manager)
            comment.db_manager = db_manager
            return comment
        return None
    
    def delete_by_post_id(post_id: str, db_manager: DatabaseManager):
        """Delete all comments for a specific post"""
        conn = sqlite3.connect(db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM comments WHERE post_id = ?", (post_id,))
        
        # delete related votes
        cursor.execute("DELETE FROM comment_votes WHERE comment_id IN (SELECT id FROM comments WHERE post_id = ?)", (post_id,))
        conn.commit()
        conn.close()
    
    def delete(self):
        """Delete this comment from the database"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM comments WHERE id = ?", (self.id,))
        
        # delete related votes
        cursor.execute("DELETE FROM comment_votes WHERE comment_id = ?", (self.id,))
        conn.commit()
        conn.close()

    def add_vote(self, user: User, vote: int):
        """Add or update a vote for this comment"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO comment_votes (comment_id, user_id, vote) VALUES (?, ?, ?)",
            (self.id, user.id, vote)
        )
        conn.commit()
        conn.close()

    def is_impostor(self, user: User) -> bool:
        """Check if the user is an impostor for this comment"""
        if not self.post.competition_finished():
            return False
        roles = self.post.get_user_roles()
        return roles.get(user.id, UserRole.INNOCENT) == UserRole.IMPOSTOR
    
    def get_votes(self) -> Dict[str, Vote]:
        """Get all votes for this comment"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, vote FROM comment_votes WHERE comment_id = ?", (self.id,))
        votes = {user_id: Vote(vote) for user_id, vote in cursor.fetchall()}
        conn.close()
        return votes