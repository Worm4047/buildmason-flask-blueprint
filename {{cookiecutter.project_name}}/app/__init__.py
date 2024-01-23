# init.py

from flask import Flask
from flask_login import LoginManager
from app.models.user import db, User
from app.routes.auth import auth as auth_blueprint
from app.routes.main import main as main_blueprint

# init SQLAlchemy so we can use it later in our models
def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    
    app.register_blueprint(main_blueprint)

    return app