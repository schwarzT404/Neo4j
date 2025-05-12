from flask import Blueprint, request, jsonify
from models.comment import Comment
from models.user import User
from models.post import Post

# Création d'un blueprint pour les routes commentaire
comment_bp = Blueprint('comment_routes', __name__)

@comment_bp.route('', methods=['GET'])
def get_comments():
    """Récupère tous les commentaires"""
    try:
        comments = Comment.get_all()
        return jsonify({"success": True, "data": comments}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@comment_bp.route('/<comment_id>', methods=['GET'])
def get_comment(comment_id):
    """Récupère un commentaire par son ID"""
    try:
        comment = Comment.find_by_id(comment_id)
        if not comment:
            return jsonify({
                "success": False,
                "error": "Commentaire non trouvé"
            }), 404
            
        return jsonify({
            "success": True,
            "data": comment.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@comment_bp.route('/<comment_id>', methods=['PUT'])
def update_comment(comment_id):
    """Met à jour un commentaire"""
    try:
        data = request.json
        if not data or 'content' not in data:
            return jsonify({
                "success": False,
                "error": "Le champ content est requis"
            }), 400
            
        comment = Comment.find_by_id(comment_id)
        if not comment:
            return jsonify({
                "success": False,
                "error": "Commentaire non trouvé"
            }), 404
            
        # Mise à jour du commentaire
        comment.update(content=data['content'])
        
        return jsonify({
            "success": True,
            "message": "Commentaire mis à jour avec succès",
            "data": comment.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@comment_bp.route('/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """Supprime un commentaire"""
    try:
        comment = Comment.find_by_id(comment_id)
        if not comment:
            return jsonify({
                "success": False,
                "error": "Commentaire non trouvé"
            }), 404
            
        comment.delete()
        
        return jsonify({
            "success": True,
            "message": "Commentaire supprimé avec succès"
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@comment_bp.route('/<comment_id>/like', methods=['POST'])
def like_comment(comment_id):
    """Ajoute un like à un commentaire"""
    try:
        data = request.json
        if not data or 'user_id' not in data:
            return jsonify({
                "success": False,
                "error": "L'ID de l'utilisateur est requis"
            }), 400
            
        comment = Comment.find_by_id(comment_id)
        if not comment:
            return jsonify({
                "success": False,
                "error": "Commentaire non trouvé"
            }), 404
            
        user = User.find_by_id(data['user_id'])
        if not user:
            return jsonify({
                "success": False,
                "error": "Utilisateur non trouvé"
            }), 404
            
        comment.add_like(data['user_id'])
        
        return jsonify({
            "success": True,
            "message": "Like ajouté avec succès"
        }), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@comment_bp.route('/<comment_id>/like', methods=['DELETE'])
def unlike_comment(comment_id):
    """Retire un like d'un commentaire"""
    try:
        data = request.json
        if not data or 'user_id' not in data:
            return jsonify({
                "success": False,
                "error": "L'ID de l'utilisateur est requis"
            }), 400
            
        comment = Comment.find_by_id(comment_id)
        if not comment:
            return jsonify({
                "success": False,
                "error": "Commentaire non trouvé"
            }), 404
            
        user = User.find_by_id(data['user_id'])
        if not user:
            return jsonify({
                "success": False,
                "error": "Utilisateur non trouvé"
            }), 404
            
        comment.remove_like(data['user_id'])
        
        return jsonify({
            "success": True,
            "message": "Like retiré avec succès"
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500