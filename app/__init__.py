from sqlite3 import Connection as SQLite3Connection
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.engine import Engine
from flask_migrate import Migrate
from dotenv import load_dotenv
from sqlalchemy import event
from flask import Flask
import cloudinary
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
load_dotenv()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    from app.models import Signup
    from app.routes.auth import auth_bp
    from app.routes.home import home_bp
    from app.routes.settings import settings_bp
    from app.routes.dashboard import dashboard_bp

    @login_manager.user_loader
    def load_user(user_id):
        return Signup.query.get(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(dashboard_bp)

    return app
