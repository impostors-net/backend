import uuid

import user

class Post:
    def __init__(self, post_uuid: uuid.UUID, content: str, owner: user.User):
        self.post_uuid = post_uuid
        self.content = content
        self.owner = owner

    def get_owner(self):
        return self.owner

    def get_content(self):
        return self.content