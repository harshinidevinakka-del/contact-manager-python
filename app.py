from flask import Flask
from flask_cors import CORS
from models import db
from routes.contacts import contacts_bp
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///contacts.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "change-this-in-production"

    CORS(app)
    db.init_app(app)

    app.register_blueprint(contacts_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()
        logging.info("Database ready.")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
