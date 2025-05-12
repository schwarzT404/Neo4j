from flask import Flask, jsonify
from flask_cors import CORS
from config import DEBUG, SECRET_KEY
from services.db_service import get_db

# Import des routes
from routes.user_routes import user_bp
from routes.post_routes import post_bp
from routes.comment_routes import comment_bp

# Initialisation de l'application Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG'] = DEBUG

# Activation de CORS
CORS(app)

# Enregistrement des blueprints
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(post_bp, url_prefix='/posts')
app.register_blueprint(comment_bp, url_prefix='/comments')

@app.route('/')
def index():
    """Page d'accueil de l'API"""
    return jsonify({
        "message": "Bienvenue sur l'API Neo4j avec Flask",
        "version": "1.0.0",
        "endpoints": {
            "users": "/users",
            "posts": "/posts",
            "comments": "/comments"
        }
    })

@app.route('/test-db')
def test_db():
    """Test de la connexion à Neo4j"""
    try:
        db = get_db()
        # Exécuter une requête simple
        result = db.run("MATCH (n) RETURN count(n) AS count").data()
        node_count = result[0]["count"] if result else 0
        
        return jsonify({
            "status": "success",
            "message": "Connexion à Neo4j établie avec succès",
            "node_count": node_count
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erreur de connexion à Neo4j: {str(e)}"
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Gestionnaire pour les routes non trouvées"""
    return jsonify({"error": "Route non trouvée"}), 404

@app.errorhandler(500)
def server_error(error):
    """Gestionnaire pour les erreurs serveur"""
    return jsonify({"error": "Erreur interne du serveur"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)