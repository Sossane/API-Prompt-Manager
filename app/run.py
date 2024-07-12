# from app import create_app


# app = create_app()


# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# Configuration pour JWT
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

jwt = JWTManager(app)

from app.users import user_bp
# Enregistrement des blueprints
app.register_blueprint(user_bp, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
