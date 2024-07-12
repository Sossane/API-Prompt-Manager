from flask import Blueprint, request, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from .db import get_db

vote_bp = Blueprint('vote', __name__)

@vote_bp.route('/vote', methods=['POST'])
@jwt_required()
def vote():
    db = get_db()
    user_id = get_jwt_identity()
    vote = request.json['vote']
    if vote == 'up':
        db.execute('UPDATE posts SET upvotes = upvotes + 1 WHERE id = ?', (request.json['post_id']))
    elif vote == 'down':
        db.execute('UPDATE posts SET downvotes = downvotes + 1 WHERE id = ?', (request.json['post_id']))
        db.commit()
        return jsonify({'message': 'Vote recorded'}), 200
    else:
        return jsonify({'message': 'Invalid vote'}), 400
    
    
    
