from flask import Flask, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash
from db import get_db, close_db, init_db_command, create_admin_user
import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    DATABASE_URL = os.environ.get('DATABASE_URL') 
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    FLASK_APP = 'app'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register database functions
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_admin_user)

    @app.route('/register', methods=['POST'])
    def register():
        if request.method == 'POST':
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
                db.execute('INSERT INTO users(username, email, password, role_id) VALUES(%s, %s, %s, %s);',
                           (username, email, hashed_password, 1))
                db.commit()
                return jsonify({'message': 'User registered successfully'}), 201

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
