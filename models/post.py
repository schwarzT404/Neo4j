import uuid
from datetime import datetime
from py2neo import Node, Relationship
from services.db_service import get_db
from models.user import User

class Post:
    def __init__(self, title, content, author_id, post_id=None, created_at=None):
        self.id = post_id or str(uuid.uuid4())
        self.title = title
        self.content = content
        self.author_id = author_id
        self.created_at = created_at or datetime.now().timestamp()
    
    def to_dict(self):
        """Convertit le post en dictionnaire"""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author_id": self.author_id,
            "created_at": self.created_at
        }
    
    def save(self):
        """Enregistre le post dans la base de données"""
        db = get_db()
        
        # Exécuter une transaction pour créer le post et sa relation avec l'auteur
        result = db.run("""
            MATCH (author:User {id: $author_id})
            CREATE (p:Post {id: $id, title: $title, content: $content, created_at: $created_at})
            CREATE (author)-[r:CREATED]->(p)
            RETURN p
        """, id=self.id, title=self.title, content=self.content, 
             created_at=self.created_at, author_id=self.author_id).data()
        
        return self
    
    def update(self, title=None, content=None):
        """Met à jour les informations du post"""
        db = get_db()
        
        # Mettre à jour uniquement les champs fournis
        if title:
            self.title = title
        if content:
            self.content = content
            
        # Mise à jour dans la base de données
        db.run("""
            MATCH (p:Post {id: $id})
            SET p.title = $title, p.content = $content
            RETURN p
        """, id=self.id, title=self.title, content=self.content)
        
        return self
    
    def delete(self):
        """Supprime le post et ses relations"""
        db = get_db()
        # Suppression du post et de toutes ses relations
        db.run("""
            MATCH (p:Post {id: $id})
            DETACH DELETE p
        """, id=self.id)
        
        return True
    
    def add_like(self, user_id):
        """Ajoute un like au post"""
        db = get_db()
        result = db.run("""
            MATCH (u:User {id: $user_id}), (p:Post {id: $post_id})
            MERGE (u)-[r:LIKES]->(p)
            RETURN r
        """, user_id=user_id, post_id=self.id).data()
        
        return bool(result)
    
    def remove_like(self, user_id):
        """Retire un like du post"""
        db = get_db()
        db.run("""
            MATCH (u:User {id: $user_id})-[r:LIKES]->(p:Post {id: $post_id})
            DELETE r
        """, user_id=user_id, post_id=self.id)
        
        return True
    
    def get_likes_count(self):
        """Récupère le nombre de likes du post"""
        db = get_db()
        result = db.run("""
            MATCH (u:User)-[:LIKES]->(p:Post {id: $id})
            RETURN count(u) as likes_count
        """, id=self.id).data()
        
        return result[0]['likes_count'] if result else 0
    
    def get_comments(self):
        """Récupère les commentaires du post"""
        from models.comment import Comment  # Import ici pour éviter les imports circulaires
        
        db = get_db()
        results = db.run("""
            MATCH (p:Post {id: $id})-[:HAS_COMMENT]->(c:Comment)
            RETURN c, p.id as post_id
        """, id=self.id).data()
        
        return [Comment(
            comment_id=result['c']['id'],
            content=result['c']['content'],
            author_id=result['c']['author_id'],
            post_id=result['post_id'],
            created_at=result['c']['created_at']
        ).to_dict() for result in results]
    
    @classmethod
    def find_by_id(cls, post_id):
        """Trouve un post par son ID"""
        db = get_db()
        result = db.run("""
            MATCH (p:Post {id: $id})
            MATCH (author:User)-[:CREATED]->(p)
            RETURN p, author.id as author_id
        """, id=post_id).data()
        
        if not result:
            return None
            
        post_data = result[0]['p']
        author_id = result[0]['author_id']
        
        return cls(
            post_id=post_data['id'],
            title=post_data['title'],
            content=post_data['content'],
            author_id=author_id,
            created_at=post_data['created_at']
        )
    
    @classmethod
    def get_all(cls):
        """Récupère tous les posts"""
        db = get_db()
        results = db.run("""
            MATCH (p:Post)
            MATCH (author:User)-[:CREATED]->(p)
            RETURN p, author.id as author_id
        """).data()
        
        return [cls(
            post_id=result['p']['id'],
            title=result['p']['title'],
            content=result['p']['content'],
            author_id=result['author_id'],
            created_at=result['p']['created_at']
        ).to_dict() for result in results]
    
    @classmethod
    def get_user_posts(cls, user_id):
        """Récupère tous les posts d'un utilisateur"""
        db = get_db()
        results = db.run("""
            MATCH (author:User {id: $user_id})-[:CREATED]->(p:Post)
            RETURN p, author.id as author_id
        """, user_id=user_id).data()
        
        return [cls(
            post_id=result['p']['id'],
            title=result['p']['title'],
            content=result['p']['content'],
            author_id=result['author_id'],
            created_at=result['p']['created_at']
        ).to_dict() for result in results]