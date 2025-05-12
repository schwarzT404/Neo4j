import uuid
from datetime import datetime
from py2neo import Node, Relationship
from services.db_service import get_db

class User:
    def __init__(self, name, email, user_id=None, created_at=None):
        self.id = user_id or str(uuid.uuid4())
        self.name = name
        self.email = email
        self.created_at = created_at or datetime.now().timestamp()
    
    def to_dict(self):
        """Convertit l'utilisateur en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at
        }
    
    def save(self):
        """Enregistre l'utilisateur dans la base de données"""
        db = get_db()
        # Créer un nœud avec les propriétés de l'utilisateur
        user_node = Node("User", 
                        id=self.id,
                        name=self.name,
                        email=self.email,
                        created_at=self.created_at)
        
        # Insertion du nœud dans la base de données
        db.create(user_node)
        return self
    
    def update(self, name=None, email=None):
        """Met à jour les informations de l'utilisateur"""
        db = get_db()
        # Mise à jour uniquement des champs fournis
        if name:
            self.name = name
        if email:
            self.email = email
            
        # Mise à jour dans la base de données
        db.run("""
            MATCH (u:User {id: $id})
            SET u.name = $name, u.email = $email
            RETURN u
        """, id=self.id, name=self.name, email=self.email)
        
        return self
    
    def delete(self):
        """Supprime l'utilisateur et ses relations"""
        db = get_db()
        # Suppression de l'utilisateur et de toutes ses relations
        db.run("""
            MATCH (u:User {id: $id})
            DETACH DELETE u
        """, id=self.id)
        
        return True
    
    def add_friend(self, friend_id):
        """Ajoute une relation d'amitié avec un autre utilisateur"""
        db = get_db()
        result = db.run("""
            MATCH (u1:User {id: $user_id}), (u2:User {id: $friend_id})
            MERGE (u1)-[r:FRIENDS_WITH]->(u2)
            RETURN r
        """, user_id=self.id, friend_id=friend_id).data()
        
        return bool(result)
    
    def remove_friend(self, friend_id):
        """Supprime une relation d'amitié"""
        db = get_db()
        db.run("""
            MATCH (u1:User {id: $user_id})-[r:FRIENDS_WITH]-(u2:User {id: $friend_id})
            DELETE r
        """, user_id=self.id, friend_id=friend_id)
        
        return True
    
    def is_friend_with(self, friend_id):
        """Vérifie si l'utilisateur est ami avec un autre utilisateur"""
        db = get_db()
        result = db.run("""
            MATCH (u1:User {id: $user_id})-[:FRIENDS_WITH]-(u2:User {id: $friend_id})
            RETURN u2
        """, user_id=self.id, friend_id=friend_id).data()
        
        return bool(result)
    
    def get_friends(self):
        """Récupère la liste des amis de l'utilisateur"""
        db = get_db()
        results = db.run("""
            MATCH (u:User {id: $id})-[:FRIENDS_WITH]-(friend:User)
            RETURN friend
        """, id=self.id).data()
        
        return [User(
            user_id=result['friend']['id'],
            name=result['friend']['name'],
            email=result['friend']['email'],
            created_at=result['friend']['created_at']
        ).to_dict() for result in results]
    
    def get_mutual_friends(self, other_id):
        """Récupère les amis en commun avec un autre utilisateur"""
        db = get_db()
        results = db.run("""
            MATCH (u1:User {id: $user_id})-[:FRIENDS_WITH]-(mutual:User)-[:FRIENDS_WITH]-(u2:User {id: $other_id})
            RETURN mutual
        """, user_id=self.id, other_id=other_id).data()
        
        return [User(
            user_id=result['mutual']['id'],
            name=result['mutual']['name'],
            email=result['mutual']['email'],
            created_at=result['mutual']['created_at']
        ).to_dict() for result in results]
    
    @classmethod
    def find_by_id(cls, user_id):
        """Trouve un utilisateur par son ID"""
        db = get_db()
        result = db.run("""
            MATCH (u:User {id: $id})
            RETURN u
        """, id=user_id).data()
        
        if not result:
            return None
            
        user_data = result[0]['u']
        return cls(
            user_id=user_data['id'],
            name=user_data['name'],
            email=user_data['email'],
            created_at=user_data['created_at']
        )
    
    @classmethod
    def find_by_email(cls, email):
        """Trouve un utilisateur par son email"""
        db = get_db()
        result = db.run("""
            MATCH (u:User {email: $email})
            RETURN u
        """, email=email).data()
        
        if not result:
            return None
            
        user_data = result[0]['u']
        return cls(
            user_id=user_data['id'],
            name=user_data['name'],
            email=user_data['email'],
            created_at=user_data['created_at']
        )
    
    @classmethod
    def get_all(cls):
        """Récupère tous les utilisateurs"""
        db = get_db()
        results = db.run("""
            MATCH (u:User)
            RETURN u
        """).data()
        
        return [cls(
            user_id=result['u']['id'],
            name=result['u']['name'],
            email=result['u']['email'],
            created_at=result['u']['created_at']
        ).to_dict() for result in results]