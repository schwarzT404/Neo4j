from flask import Blueprint, request, jsonify
from models.post import Post
from models.user import User
from models.comment import Comment

# Création d'un blueprint pour les routes post
post_bp = Blueprint('post_routes', __name__)

@post_bp.route('', methods=['GET'])
def get_posts():
    """Récupère tous les posts"""
    try:
        posts = Post.get_all()
        return jsonify({"success": True, "data": posts}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@post_bp.route('/<post_id>', methods=['GET'])
def get_post(post_id):
    """Récupère un post par son ID"""
    try:
        post = Post.find_by_id(post_id)
        if not post:
            return jsonify({
                "success": False,
                "error": "Post non trouvé"
            }), 404
            
        return jsonify({
            "success": True,
            "data": post.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@post_bp.route('/<post_id>', methods=['PUT'])
def update_post(post_id):
    """Met à jour un post"""
    try:
        data = request.json
        if not data:
            return jsonify({
                "success": False,
                "error": "Aucune donnée fournie"
            }), 400
            
        post = Post.find_by_id(post_id)
        if not post:
            return jsonify({
                "success": False,
                "error": "Post non trouvé"
            }), 404
            
        # Mise à jour du post
        post.update(
            title=data.get('title', post.title),
            content=data.get('content', post.content)
        )
        
        return jsonify({
            "success": True,
            "message": "Post mis à jour avec succès",
            "data": post.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@post_bp.route('/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Supprime un post"""
    try:
        post = Post.find_by_id(post_id)
        if not post:
            return jsonify({
                "success": False,
                "error": "Post non trouvé"
            }), 404
            
        post.delete()
        
        return jsonify({
            "success": True,
            "message": "Post supprimé avec succès"
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@post_bp.route('/<post_id>/like', methods=['POST'])
def like_post(post_id):
    """Ajoute un like à un post"""
    try:
        data = request.json
        if not data or 'user_id' not in data:
            return jsonify({
                "success": False,
                "error": "L'ID de l'utilisateur est requis"
            }), 400
            
        post = Post.find_by_id(post_id)
        if not post:
            return jsonify({
                "success": False,
                "error": "Post non trouvé"
            }), 404
            
        user = User.find_by_id(data['user_id'])
        if not user:
            return jsonify({
                "success": False,
                "error": "Utilisateur non trouvé"
            }), 404
            
        post.add_like(data['user_id'])
        
        return jsonify({
            "success": True,
            "message": "Like ajouté avec succès"
        }), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@post_bp.route('/<post_id>/like', methods=['DELETE'])
def unlike_post(post_id):
    """Retire un like d'un post"""
    try:
        data = request.json
        if not data or 'user_id' not in data:
            return jsonify({
                "success": False,
                "error": "L'ID de l'utilisateur est requis"
            }), 400
            
        post = Post.find_by_id(post_id)
        if not post:
            return jsonify({
                "success": False,
                "error": "Post non trouvé"
            }), 404
            
        user = User.find_by_id(data['user_id'])
        if not user:
            return jsonify({
                "success": False,
                "error": "Utilisateur non trouvé"
            }), 404
            
        post.remove_like(data['user_id'])
        
        return jsonify({
            "success": True,
            "message": "Like retiré avec succès"
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@post_bp.route('/<post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    """Récupère les commentaires d'un post"""
    try:
        post = Post.find_by_id(post_id)
        if not post:
            return jsonify({
                "success": False,
                "error": "Post non trouvé"
            }), 404
            
        comments = Comment.get_post_comments(post_id)
        
        return jsonify({
            "success": True,
            "data": comments
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@post_bp.route('/<post_id>/comments', methods=['POST'])
def add_comment(post_id):
    """Ajoute un commentaire à un post"""
    try:
        data = request.json
        if not data or 'content' not in data or 'user_id' not in data:
            return jsonify({
                "success": False,
                "error": "Les champs content et user_id sont requis"
            }), 400
            
        post = Post.find_by_id(post_id)
        if not post:
            return jsonify({
                "success": False,
                "error": "Post non trouvé"
            }), 404
            
        user = User.find_by_id(data['user_id'])
        if not user:
            return jsonify({
                "success": False,
                "error": "Utilisateur non trouvé"
            }), 404
            
        # Création du commentaire
        comment = Comment(
            content=data['content'],
            author_id=data['user_id'],
            post_id=post_id
        )
        comment.save()
        
        return jsonify({
            "success": True,
            "message": "Commentaire ajouté avec succès",
            "data": comment.to_dict()
        }), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@post_bp.route('/<post_id>/comments/<comment_id>', methods=['DELETE'])
def delete_post_comment(post_id, comment_id):
    """Supprime un commentaire d'un post"""
    try:
        post = Post.find_by_id(post_id)
        if not post:
            return jsonify({
                "success": False,
                "error": "Post non trouvé"
            }), 404
            
        comment = Comment.find_by_id(comment_id)
        if not comment:
            return jsonify({
                "success": False,
                "error": "Commentaire non trouvé"
            }), 404
            
        # Vérifier que le commentaire appartient bien au post
        if comment.post_id != post_id:
            return jsonify({
                "success": False,
                "error": "Ce commentaire n'appartient pas à ce post"
            }), 400
            
        comment.delete()
        
        return jsonify({
            "success": True,
            "message": "Commentaire supprimé avec succès"
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500