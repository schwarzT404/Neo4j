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
    
    @staticmethod
    def get_all():
        """Récupère tous les commentaires depuis la base de données"""
        db = get_db()
        result = db.run("MATCH (c:Comment) RETURN c").data()
        comments = []
        
        for record in result:
            node = record['c']
            comment = Comment(
                content=node['content'],
                author_id=node['author_id'],
                post_id=node['post_id'],
                comment_id=node['id'],
                created_at=node['created_at']
            )
            comments.append(comment.to_dict())
            
        return comments
        
    def to_dict(self):
        """Convertit l'instance en dictionnaire"""
        return {
            "id": self.id,
            "content": self.content,
            "author_id": self.author_id,
            "post_id": self.post_id,
            "created_at": self.created_at
        }