from py2neo import Graph
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

class DatabaseService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
            cls._instance.graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
            cls._instance._create_constraints()
        return cls._instance
    
    def _create_constraints(self):
        """Crée les contraintes et index nécessaires sur les noeuds"""
        # Contrainte d'unicité sur l'email des utilisateurs
        try:
            self.graph.run("CREATE CONSTRAINT user_email IF NOT EXISTS ON (u:User) ASSERT u.email IS UNIQUE")
        except Exception as e:
            print(f"Erreur lors de la création de la contrainte d'email: {e}")
            
        # On peut ajouter d'autres contraintes ou index selon les besoins

    def get_db(self):
        """Retourne l'instance de connexion à la base de données"""
        return self.graph

# Création d'une instance singleton
db_service = DatabaseService()

def get_db():
    """Fonction utilitaire pour obtenir la connexion à la base de données"""
    return db_service.get_db()