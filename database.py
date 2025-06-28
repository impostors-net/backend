import sqlite3
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

class UserRole(Enum):
    IMPOSTOR = True
    INNOCENT = False

class Vote(Enum):
    UPVOTE = 1
    DOWNVOTE = -1

class DatabaseManager:
    def __init__(self, db_path: str = "app.db"):
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
                handle TEXT UNIQUE NOT NULL
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
    def __init__(self, display_name: str, handle: str, db_manager: DatabaseManager):
        if User.get_by_handle(handle, db_manager):
            raise ValueError(f"User with handle '{handle}' already exists.")
        self.id = str(uuid.uuid4())
        self.display_name = display_name
        self.handle = handle
        self.db_manager = db_manager
        self._save()
    
    def _save(self):
        """Save user to database"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (id, display_name, handle) VALUES (?, ?, ?)",
            (self.id, self.display_name, self.handle)
        )
        conn.commit()
        conn.close()
    
    @classmethod
    def get_by_id(cls, user_id: str, db_manager: DatabaseManager) -> Optional['User']:
        """Retrieve user by ID"""
        conn = sqlite3.connect(db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT display_name, handle FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            user = cls.__new__(cls)
            user.id = user_id
            user.display_name = result[0]
            user.handle = result[1]
            user.db_manager = db_manager
            return user
        return None

    @classmethod
    def get_by_handle(cls, handle: str, db_manager: DatabaseManager) -> Optional['User']:
        """Retrieve user by handle"""
        conn = sqlite3.connect(db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, display_name FROM users WHERE handle = ?", (handle,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            user = cls.__new__(cls)
            user.id = result[0]
            user.display_name = result[1]
            user.handle = handle
            user.db_manager = db_manager
            return user
        return None
    
    def get_posts(self) -> List['Post']:
        """Get all posts by this user"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM posts WHERE author_id = ?", (self.id,))
        post_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return [Post.get_by_id(post_id, self.db_manager) for post_id in post_ids]

class Post:
    def __init__(self, content: str, author: User):
        self.id = str(uuid.uuid4())
        self.content = content
        self.created_at = datetime.now().isoformat()
        self.author = author
        self.db_manager = author.db_manager
        self._save()
    
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
    
    def get_comments(self) -> List['Comment']:
        """Get all comments for this post"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM comments WHERE post_id = ?", (self.id,))
        comment_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return [Comment.get_by_id(comment_id, self.db_manager) for comment_id in comment_ids]
    
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

class Comment:
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
    
    def add_vote(self, user: User, vote: Vote):
        """Add or update a vote for this comment"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO comment_votes (comment_id, user_id, vote) VALUES (?, ?, ?)",
            (self.id, user.id, vote.value)
        )
        conn.commit()
        conn.close()
    
    def get_votes(self) -> Dict[str, Vote]:
        """Get all votes for this comment"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, vote FROM comment_votes WHERE comment_id = ?", (self.id,))
        votes = {user_id: Vote(vote) for user_id, vote in cursor.fetchall()}
        conn.close()
        return votes