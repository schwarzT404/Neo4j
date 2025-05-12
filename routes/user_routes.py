from flask import Blueprint, request, jsonify
from models.user import User
from models.post import Post

# Création d'un blueprint pour les routes utilisateur
user_bp = Blueprint('user_routes', __name__)

@user_bp.route('', methods=['GET'])
def get_users():
    """Récupère tous les utilisateurs"""
    try:
        users = User.get_all()
        return jsonify({"success": True, "data": users}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@user_bp.route('', methods=['POST'])
def create_user():
    """Crée un nouvel utilisateur"""
    try:
        data = request.json
        # Vérification des champs requis
        if not data or 'name' not in data or 'email' not in data:
            return jsonify({
                "success": False,
                "error": "Les champs name et email sont requis"
            }), 400
            
        # Vérification si l'email existe déjà
        existing_user = User.find_by_email(data['email'])
        if existing_user:
            return jsonify({
                "success": False,
                "error": "Un utilisateur avec cet email existe déjà"
            }), 409
        
        # Création de l'utilisateur
        user = User(name=data['name'], email=data['email'])
        user.save()
        
        return jsonify({
            "success": True,
            "message": "Utilisateur créé avec succès",
            "data": user.to_dict()
        }), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """Récupère un utilisateur par son ID"""
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({
                "success": False,
                "error": "Utilisateur non trouvé"
            }), 404
            
        return jsonify({
            "success": True,
            "data": user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@user_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Met à jour un utilisateur"""
    try:
        data = request.json
        if not data:
            return jsonify({
                "success": False,
                "error": "Aucune donnée fournie"
            }), 400
            
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({
                "success": False,
                "error": "Utilisateur non trouvé"
            }), 404
            
        # Vérification si l'email est déjà utilisé par un autre utilisateur
        if 'email' in data and data['email'] != user.email:
            existing_user = User.find_by_email(data['email'])
            if existing_user and existing_user.id != user_id:
                return jsonify({
                    "success": False,
                    "error": "Cet email est déjà utilisé par un autre utilisateur"
                }), 409
                
        # Mise à jour de l'utilisateur
        user.update(
            name=data.get('name', user.name),
            email=data.get('email', user.email)
        )
        
        return jsonify({
            "success": True,
            "message": "Utilisateur mis à jour avec succès",
            "data": user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Supprime un utilisateur"""
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({
                "success": False,
                "error": "Utilisateur non trouvé"
            }), 404
            
        user.delete()
        
        return jsonify({
            "success": True,
            "message": "Utilisateur supprimé avec succès"
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@user_bp.route('/<user_id>/friends', methods=['GET'])
def get_friends(user_id):
    """Récupère les amis d'un utilisateur"""
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({
                "success": False,
                "error": "Utilisateur non trouvé"
            }), 404
            
        friends = user.get_friends()
        
        return jsonify({
            "success": True,
            "data": friends
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@user_bp.route('/<user_id>/friends', methods=['POST'])
def add_friend(user_id):
    """Ajoute un ami à l'utilisateur"""
    try:
        data = request.json
        if not data or 'friend_id' not in data:
            return jsonify({
                "success": False,
                "error": "L'ID de l'ami est requis"
            }), 400
            
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({
                "success": False,
                "error": "Utilisateur non trouvé"
            }), 404
            
        friend = User.find_by_id(data['friend_id'])
        if not friend:
            return jsonify({
                "success": False,
                "error": "Ami non trouvé"
            }), 404
            
        # Vérifier si déjà amis
        if user.is_friend_with(data['friend_id']):
            return jsonify({
                "success": False,
                "error": "Ces utilisateurs sont déjà amis"
            }), 409
            
        user.add_friend(data['friend_id'])
        
        return jsonify({
            "success": True,
            "message": "Ami ajouté avec succès"
        }), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@user_bp.route('/<user_id>/friends/<friend_id>', methods=['GET'])
def check_friendship(user_id, friend_id):
    """Vérifie si deux utilisateurs sont amis"""
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({
                "success": False,
                "error": "Utilisateur non trouvé"
            }), 404
            
        friend = User.find_by_id(friend_id)
        if not friend:
            return jsonify({
                "success": False,
                "error": "Ami non trouvé"
            }), 404
            
        is_friend = user.is_friend_with(friend_id)
        
        return jsonify({
            "success": True,
            "data": {
                "is_friend": is_friend
            }
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@user_bp.route('/<user_id>/friends/<friend_id>', methods=['DELETE'])
def remove_friend(user_id, friend_id):
    """Supprime une relation d'amitié"""
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({
                "success": False,
                "error": "Utilisateur non trouvé"
            }), 404
            
        friend = User.find_by_id(friend_id)
        if not friend:
            return jsonify({
                "success": False,
                "error": "Ami non trouvé"
            }), 404
            
        # Vérifier si amis
        if not user.is_friend_with(friend_id):
            return jsonify({
                "success": False,
                "error": "Ces utilisateurs ne sont pas amis"
            }), 404
            
        user.remove_friend(friend_id)
        
        return jsonify({
            "success": True,
            "message": "Relation d'amitié supprimée avec succès"
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@user_bp.route('/<user_id>/mutual-friends/<other_id>', methods=['GET'])
def get_mutual_friends(user_id, other_id):
    """Récupère les amis en commun entre deux utilisateurs"""
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({
                "success": False,
                "error": "Utilisateur non trouvé"
            }), 404
            
        other_user = User.find_by_id(other_id)
        if not other_user:
            return jsonify({
                "success": False,
                "error": "Autre utilisateur non trouvé"
            }), 404
            
        mutual_friends = user.get_mutual_friends(other_id)
        
        return jsonify({
            "success": True,
            "data": mutual_friends
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@user_bp.route('/<user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    """Récupère les posts d'un utilisateur"""
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({
                "success": False,
                "error": "Utilisateur non trouvé"
            }), 404
            
        posts = Post.get_user_posts(user_id)
        
        return jsonify({
            "success": True,
            "data": posts
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@user_bp.route('/<user_id>/posts', methods=['POST'])
def create_post(user_id):
    """Crée un nouveau post pour un utilisateur"""
    try:
        data = request.json
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({
                "success": False,
                "error": "Les champs title et content sont requis"
            }), 400
            
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({
                "success": False,
                "error": "Utilisateur non trouvé"
            }), 404
            
        # Création du post
        post = Post(
            title=data['title'],
            content=data['content'],
            author_id=user_id
        )
        post.save()
        
        return jsonify({
            "success": True,
            "message": "Post créé avec succès",
            "data": post.to_dict()
        }), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500