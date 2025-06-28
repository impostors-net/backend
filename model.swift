// This file was used to sketch the database schema in a usable language.

import SwiftData
import Foundation

@Model class User {
    @Attribute(.primaryKey) var id: UUID
    var displayName: String
    @Attribute(.unique) var handle: String
    @Relationship(deleteRule: .cascade) var posts: [Post]

    init(name: String, handle: String) {
        self.id = UUID()
        self.name = name
        self.handle = handle
        self.posts = []
    }
}

enum UserRole: Bool {
    case impostor = true
    case innocent = false
}

@Model class Post {
    @Attribute(.primaryKey) var id: UUID
    var content: String
    var createdAt: Date
    @Relationship(inverse: \User.posts) var author: User
    @Relationship(deleteRule: .cascade) var comments: [Comment]
    var roles: [User: UserRole] = [:]

    init(content: String, author: User) {
        self.id = UUID()
        self.content = content
        self.createdAt = Date()
        self.author = author
        self.comments = []
    }
}

@Model class Comment {
    enum Vote: Int {
        case upvote = 1
        case downvote = -1
    }
    @Attribute(.primaryKey) var id: UUID
    var content: String
    var createdAt: Date
    @Relationship(inverse: \Post.comments) var post: Post
    var author: User
    var votes: [User: Vote] = [:]

    init(content: String, post: Post, author: User) {
        self.id = UUID()
        self.content = content
        self.createdAt = Date()
        self.post = post
        self.author = author
    }
}