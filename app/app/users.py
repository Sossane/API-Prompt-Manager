# from flask import Blueprint, request, jsonify, flash
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
# from .db import get_db

# user_bp = Blueprint('user', __name__)


# @user_bp.route('/register', methods=['POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         confirm_password = request.form['confirm_password']
#         if password != confirm_password:
#             flash('Password not conform.')
#             return jsonify({'error': 'Password not conform.'}), 400
#         else:
#             db = get_db()
#             hashed_password = generate_password_hash(password=password)
#             db.execute('INSERT INTO users(username, email, password, role_id) VALUES(%s, %s, %s, %s);', (username, email, hashed_password, 1))
#             db.commit()
#             return jsonify({'message': 'User registered successfully'}), 201
        

# @user_bp.route('/getter', methods=['GET'])
# def getter():
#     if request.method == 'GET':
#         db = get_db()
#         users = db.execute('SELECT * FROM users;').fetchall()
#         return jsonify(users), 200
#     else:
#         return jsonify({'error': 'Method not allowed'}), 405
    

# @user_bp.route('/getter_id/<int:id>', methods=['GET'])
# def getter_id(id):
#     if request.method == 'GET':
#         db = get_db()
#         user = db.execute('SELECT * FROM users WHERE id = %s;', (id,)).fetchone()
#         return jsonify(user), 200
#     else:
#         return jsonify({'error': 'Method not allowed'}), 405


# @user_bp.route('/edit/<int:id>', methods=['PUT'])
# def edit(id):
#     if request.method == 'PUT':
#         db = get_db()
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         confirm_password = request.form['confirm_password']
#         if password != confirm_password:
#             flash('Password not conform.')
#             return jsonify({'error': 'Password not conform.'}), 400
#         else:
#             hashed_password = generate_password_hash(password=password)
#             db.execute('UPDATE users SET username=%s, email=%s, password=%s WHERE id=%s;', (username, email, hashed_password, id))
#             db.commit()
#             return jsonify({'message': 'User updated successfully'}), 200


# @user_bp.route('/delete/<int:id>', methods=['DELETE'])
# def delete(id):
#     if request.method == 'DELETE':
#         db = get_db()
#         db.execute('DELETE FROM users WHERE id=%s;', (id,))
#         db.commit()
#         return jsonify({'message': 'User deleted successfully'}), 200
#     else:
#         return jsonify({'error': 'Method not allowed'}), 405
    

# @user_bp.route('/login', methods=['POST'])
# def login():
#     db = get_db()
#     username = request.form['username']
#     password = request.form['password']
#     user = db.execute('SELECT * FROM users WHERE username=%s;', (username,)).fetchone()
#     if user and check_password_hash(user['password'], password):
#         access_token = create_access_token(identity={'id': user['id'], 'username': user['username']})
#         refresh_token = create_refresh_token(identity={'id': user['id'], 'username': user['username']})
#         return jsonify({
#             'access_token': access_token,
#             'refresh_token': refresh_token
#         }), 200
#     else:
#         return jsonify({'error': 'Invalid username or password'}), 401
    

# @user_bp.route('/protected', methods=['GET'])
# @jwt_required()
# def protected():
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200


# @user_bp.route('/refresh', methods=['POST'])
# @jwt_required(refresh=True)
# def refresh():
#     current_user = get_jwt_identity()
#     new_access_token = create_access_token(identity=current_user)
#     return jsonify(access_token=new_access_token), 200


from flask import Blueprint, request, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from .db import get_db
from .roles_required import roles_required  # Importer le décorateur

user_bp = Blueprint('user', __name__)

# Route pour tester le rôle admin
@user_bp.route('/admin', methods=['GET'])
@jwt_required()
@roles_required(1)  # Utiliser le décorateur avec l'ID de rôle admin
def admin_only():
    return jsonify({'message': 'Welcome, admin!'}), 200


@user_bp.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    if password != confirm_password:
        flash('Password not conform.')
        return jsonify({'error': 'Password not conform.'}), 400
    else:
        db = get_db()
        hashed_password = generate_password_hash(password=password)
        db.execute('INSERT INTO users(username, email, password, role_id) VALUES(%s, %s, %s, %s);', (username, email, hashed_password, 2))  # role_id 2 pour utilisateur
        db.commit()
        return jsonify({'message': 'User registered successfully'}), 201

@user_bp.route('/create_user', methods=['POST'])
@jwt_required()
@roles_required(1)  # Seuls les admins peuvent créer des utilisateurs
def create_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    if password != confirm_password:
        return jsonify({'error': 'Password not conform.'}), 400
    db = get_db()
    hashed_password = generate_password_hash(password=password)
    db.execute('INSERT INTO users(username, email, password, role_id) VALUES(%s, %s, %s, %s);', (username, email, hashed_password, 2))  # role_id 2 pour utilisateur normal
    db.commit()
    return jsonify({'message': 'User created successfully'}), 201

@user_bp.route('/getter', methods=['GET'])
@jwt_required()
@roles_required(1)  # Seuls les admins peuvent obtenir les utilisateurs
def getter():
    db = get_db()
    users = db.execute('SELECT * FROM users;').fetchall()
    return jsonify(users), 200

@user_bp.route('/getter_id/<int:id>', methods=['GET'])
@jwt_required()
@roles_required(1, 2)  # Admins et utilisateurs peuvent obtenir l'utilisateur par ID
def getter_id(id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = %s;', (id,)).fetchone()
    return jsonify(user), 200

@user_bp.route('/edit/<int:id>', methods=['PUT'])
@jwt_required()
@roles_required(1)  # Seuls les admins peuvent modifier les utilisateurs
def edit(id):
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    if password != confirm_password:
        return jsonify({'error': 'Password not conform.'}), 400

    db = get_db()
    hashed_password = generate_password_hash(password)
    db.execute('UPDATE users SET username=%s, email=%s, password=%s WHERE id=%s;',
               (username, email, hashed_password, id))
    db.commit()
    return jsonify({'message': 'User updated successfully'}), 200

@user_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
@roles_required(1)  # Seuls les admins peuvent supprimer les utilisateurs
def delete(id):
    db = get_db()
    db.execute('DELETE FROM users WHERE id=%s;', (id,))
    db.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

@user_bp.route('/login', methods=['POST'])
def login():
    db = get_db()
    username = request.form['username']
    password = request.form['password']
    user = db.execute('SELECT * FROM users WHERE username=%s;', (username,)).fetchone()
    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity={'id': user['id'], 'username': user['username'], 'role_id': user['role_id']})  # Inclure le rôle dans le jeton
        refresh_token = create_refresh_token(identity={'id': user['id'], 'username': user['username'], 'role_id': user['role_id']})
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@user_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@user_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200
