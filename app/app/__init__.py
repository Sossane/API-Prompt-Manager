


from flask import Flask
from flask_jwt_extended import JWTManager
from .config import Config
from .db import close_db, init_db_command, create_admin_user

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt = JWTManager(app)

    # Register database functions
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_admin_user)

    # Register blueprints
    from .users import user_bp
    from .prompt import prompt_bp
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(prompt_bp, url_prefix='/prompt')

    return app







































# from flask import Flask
# from config import Config
# from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required,get_jwt_identity
# from flask import Flask, request, redirect, url_for, flash, jsonify
# from werkzeug.security import generate_password_hash , check_password_hash
# from db import get_db, close_db, init_db_command, create_admin_user
# import os

    
# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     jwt = JWTManager(app) 

#     # Register database functions
#     app.teardown_appcontext(close_db)
#     app.cli.add_command(init_db_command)
#     app.cli.add_command(create_admin_user)


# # gestion des utilisateurs

#     @app.route('/register', methods=['POST'])
#     def register():
#         if request.method == 'POST':
#             username = request.form['username']
#             email = request.form['email']
#             password = request.form['password']
#             confirm_password = request.form['confirm_password']
#             if password != confirm_password:
#                 flash('Password not conform.')
#                 return jsonify({'error': 'Password not conform.'}), 400
#             else:
#                 db = get_db()
#                 hashed_password = generate_password_hash(password=password)
#                 db.execute('INSERT INTO users(username, email, password, role_id) VALUES(%s, %s, %s, %s);',
#                            (username, email, hashed_password, 1))
#                 db.commit()
#                 return jsonify({'message': 'User registered successfully'}), 201
            
            
#     @app.route('/getter', methods=['GET'])
#     def getter():
#         if request.method == 'GET':
#             db = get_db()
#             users = db.execute('SELECT * FROM users;').fetchall()
#             return jsonify(users), 200
#         else:
#             return jsonify({'error': 'Method not allowed'}), 405
        

#     @app.route('/getter_id/<int:id>', methods=['GET'])
#     def getter_id(id):
#         if request.method == 'GET':
#             db = get_db()
#             user = db.execute('SELECT * FROM users WHERE id = %s;', (id,)).fetchone()
#             return jsonify(user), 200
#         else:
#             return jsonify({'error': 'Method not allowed'}), 405


#     @app.route('/edit/<int:id>', methods=['PUT'])
#     def edit(id):
#         if request.method == 'PUT':
#             db = get_db()
#             username = request.form['username']
#             email = request.form['email']
#             password = request.form['password']
#             confirm_password = request.form['confirm_password']
#             if password != confirm_password:
#                 flash('Password not conform.')
#                 return jsonify({'error': 'Password not conform.'}), 400
#             else:
#                 hashed_password = generate_password_hash(password=password)
#                 db.execute('UPDATE users SET username=%s, email=%s, password=%s WHERE id=%s;', (username, email, hashed_password, id))
#                 db.commit()
#                 return jsonify({'message': 'User updated successfully'}), 200 
            

#     @app.route('/delete/<int:id>', methods=['DELETE'])        
#     def delete(id):
#         if request.method == 'DELETE':
#             db = get_db()
#             db.execute('DELETE FROM users WHERE id=%s;', (id,))
#             db.commit()
#             return jsonify({'message': 'User deleted successfully'}), 200
#         else:
#             return jsonify({'error': 'Method not allowed'}), 405
        

#     @app.route('/login', methods=['POST'])
#     def login():
#         db = get_db()
#         username = request.form['username']
#         password = request.form['password']
#         user = db.execute('SELECT * FROM users WHERE username=%s;', (username,)).fetchone()
#         if user and check_password_hash(user['password'], password):
#             access_token = create_access_token(identity={'id': user['id'], 'username': user['username']})
#             refresh_token = create_refresh_token(identity={'id': user['id'], 'username': user['username']})
#             return jsonify({
#                 'access_token': access_token,
#                 'refresh_token': refresh_token
#             }), 200
#         else:
#             return jsonify({'error': 'Invalid username or password'}), 401


#     @app.route('/protected', methods=['GET'])
#     @jwt_required()
#     def protected():
#         current_user = get_jwt_identity()
#         return jsonify(logged_in_as=current_user), 200
    

#     @app.route('/refresh', methods=['POST'])
#     @jwt_required(refresh=True)
#     def refresh():
#         current_user = get_jwt_identity()
#         new_access_token = create_access_token(identity=current_user)
#         return jsonify(access_token=new_access_token), 200


# # gestion des prompts

#     @app.route('/create_prompts', methods=['POST'])
#     @jwt_required()
#     def create_prompt():
#         if request.method == 'POST':
#             db = get_db()
#             prompt = request.form['prompt']
#             user_id = get_jwt_identity()['id']
#             db.execute('INSERT INTO prompts (prompt, user_id) VALUES (%s, %s);', (prompt, user_id))
#             db.commit()
#             return jsonify({'message': 'Prompt created successfully'}), 200
#         else:
#             return jsonify({'error': 'Method not allowed'}), 405
        

#     @app.route('/get_prompts', methods=['GET'])
#     @jwt_required()
#     def get_prompts():
#         db = get_db()
#         user_id = get_jwt_identity()['id']
#         prompts = db.execute('SELECT * FROM prompts WHERE user_id=%s;', (user_id,)).fetchall()
#         return jsonify(prompts), 200
    
#     @app.route('/get_prompts/<int:id>', methods=['GET'])
#     @jwt_required()
#     def get_prompt(id):
#         db = get_db()
#         prompt = db.execute('SELECT * FROM prompts WHERE id=%s;', (id,)).fetchone()
#         return jsonify(prompt), 200
    
#     @app.route('/put_prompts/<int:id>', methods=['PUT'])
#     @jwt_required()
#     def put_prompt(id):
#         if request.method == 'PUT':
#             db = get_db()
#             prompt = request.form['prompt']
#             user_id = get_jwt_identity()['id']
#             db.execute('UPDATE prompts SET prompt=%s WHERE id=%s AND user_id=%s;',(prompt, id, user_id))
#             db.commit()
#             return jsonify({'message': 'Prompt updated successfully'}), 200
#         else:
#             return jsonify({'error': 'Method not allowed'}), 405
        

#     @app.route('/delete_prompts/<int:id>', methods=['DELETE'])
#     @jwt_required()
#     def delete_prompt(id):
#         if request.method == 'DELETE':
#             db = get_db()
#             user_id = get_jwt_identity()['id']
#             db.execute('DELETE FROM prompts WHERE id=%s AND user_id=%s;', (id, user_id))
#             db.commit()
#             return jsonify({'message': 'Prompt deleted successfully'}), 200
#         else:
#             return jsonify({'error': 'Method not allowed'}), 405




#     return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)



