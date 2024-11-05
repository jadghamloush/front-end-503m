from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
# from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/jad/Desktop/AUB/Year-4/EECE-503m/project/front-end-503m/dbapplication/testdb.db'
    app.secret_key = 'Some Key'
    app.config['SECRET_KEY'] = 'tQa$L5Cu6^*yu"V'
    app.secret_key = app.config['SECRET_KEY']
    db.init_app(app)
    CORS(app, supports_credentials=True)
    login_manager = LoginManager()
    login_manager.init_app(app)
    secret_key = app.secret_key
    # csrf = CSRFProtect(app)
    bcrypt = Bcrypt(app)
    
    from models import User
    
    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(uid)
    
    bcrypt = Bcrypt(app)
    
    from routes import register_routes
    register_routes(app, db,bcrypt)
    
    migrate = Migrate(app, db)
    
    return app