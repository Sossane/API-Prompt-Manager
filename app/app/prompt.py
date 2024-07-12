# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from .db import get_db

# prompt_bp = Blueprint('prompt', __name__)

# @prompt_bp.route('/create', methods=['POST'])
# @jwt_required()
# def create_prompt():
#     if request.method == 'POST':
#         db = get_db()
#         prompt = request.form['prompt']
#         user_id = get_jwt_identity()['id']
#         db.execute('INSERT INTO prompts (prompt, user_id) VALUES (%s, %s);', (prompt, user_id))
#         db.commit()
#         return jsonify({'message': 'Prompt created successfully'}), 200
#     else:
#         return jsonify({'error': 'Method not allowed'}), 405

# @prompt_bp.route('/get', methods=['GET'])
# @jwt_required()
# def get_prompts():
#     db = get_db()
#     user_id = get_jwt_identity()['id']
#     prompts = db.execute('SELECT * FROM prompts WHERE user_id=%s;', (user_id,)).fetchall()
#     return jsonify(prompts), 200

# @prompt_bp.route('/get/<int:id>', methods=['GET'])
# @jwt_required()
# def get_prompt(id):
#     db = get_db()
#     prompt = db.execute('SELECT * FROM prompts WHERE id=%s;', (id,)).fetchone()
#     return jsonify(prompt), 200

# @prompt_bp.route('/update/<int:id>', methods=['PUT'])
# @jwt_required()
# def update_prompt(id):
#     if request.method == 'PUT':
#         db = get_db()
#         prompt = request.form['prompt']
#         user_id = get_jwt_identity()['id']
#         db.execute('UPDATE prompts SET prompt=%s WHERE id=%s AND user_id=%s;', (prompt, id, user_id))
#         db.commit()
#         return jsonify({'message': 'Prompt updated successfully'}), 200
#     else:
#         return jsonify({'error': 'Method not allowed'}), 405

# @prompt_bp.route('/delete/<int:id>', methods=['DELETE'])
# @jwt_required()
# def delete_prompt(id):
#     if request.method == 'DELETE':
#         db = get_db()
#         user_id = get_jwt_identity()['id']
#         db.execute('DELETE FROM prompts WHERE id=%s AND user_id=%s;', (id, user_id))
#         db.commit()
#         return jsonify({'message': 'Prompt deleted successfully'}), 200
#     else:
#         return jsonify({'error': 'Method not allowed'}), 405



from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .db import get_db
from .roles_required import roles_required

prompt_bp = Blueprint('prompt', __name__)

@prompt_bp.route('/create', methods=['POST'])
@jwt_required()
@roles_required(1, 2)  # Admins et utilisateurs peuvent créer des prompts
def create_prompt():
    db = get_db()
    prompt = request.form['prompt']
    user_id = get_jwt_identity()['id']
    db.execute('INSERT INTO prompts (prompt, user_id) VALUES (%s, %s);', (prompt, user_id))
    db.commit()
    return jsonify({'message': 'Prompt created successfully'}), 200

@prompt_bp.route('/get', methods=['GET'])
@jwt_required()
@roles_required(1)  # Seuls les admins peuvent voir tous les prompts
def get_prompts():
    db = get_db()
    prompts = db.execute('SELECT * FROM prompts;').fetchall()
    return jsonify(prompts), 200

@prompt_bp.route('/get/<int:id>', methods=['GET'])
@jwt_required()
@roles_required(1, 2)  # Admins et utilisateurs peuvent voir les prompts par ID
def get_prompt(id):
    db = get_db()
    prompt = db.execute('SELECT * FROM prompts WHERE id=%s;', (id,)).fetchone()
    return jsonify(prompt), 200

@prompt_bp.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
@roles_required(1)  # Seuls les admins peuvent modifier les prompts
def update_prompt(id):
    db = get_db()
    prompt = request.form['prompt']
    db.execute('UPDATE prompts SET prompt=%s WHERE id=%s;', (prompt, id))
    db.commit()
    return jsonify({'message': 'Prompt updated successfully'}), 200

@prompt_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
@roles_required(1)  # Seuls les admins peuvent supprimer les prompts
def delete_prompt(id):
    db = get_db()
    db.execute('DELETE FROM prompts WHERE id=%s;', (id,))
    db.commit()
    return jsonify({'message': 'Prompt deleted successfully'}), 200
