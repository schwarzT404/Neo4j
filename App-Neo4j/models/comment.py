# models/comment.py
import uuid
from datetime import datetime
from py2neo import Node, Relationship
from services.db_service import get_db

class Comment:
    def __init__(self, content, author_id, post_id, comment_id=None, created_at=None):
        self.id = comment_id or str(uuid.uuid4())
        self.content = content
        self.author_id = author_id
        self.post_id = post_id
        self.created_at = created_at or datetime.now().timestamp()
    
    # All the Comment methods should follow here
    # Make sure the entire Comment class is properly defined