from flask import Flask, send_from_directory
from flask_cors import CORS
from app.extensions import Base, engine
from app.routes.question_routes import question_bp

def create_app():
    app = Flask(__name__, static_folder="../static", static_url_path="")
    CORS(app)
    Base.metadata.create_all(bind=engine)
    app.register_blueprint(question_bp)

    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    return app
