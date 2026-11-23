import logging
import os

from flask import Flask, jsonify, send_from_directory
from flask_jwt_extended import JWTManager

import db
from api import api_bp
from auth import auth_bp
from config import config_by_name


def create_app():
    app = Flask(__name__)

    environment = os.getenv(
        "FLASK_ENV",
        "development"
    )

    app.config.from_object(
        config_by_name.get(
            environment,
            config_by_name["development"]
        )
    )

    db.init_app(app)
    JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        format=(
            "%(asctime)s %(levelname)s: "
            "%(message)s"
        ),
    )

    @app.get("/")
    @app.get("/orders")
    def orders_page():
        return send_from_directory(
            ".",
            "index.html"
        )

    @app.get("/kitchen")
    def kitchen_page():
        return send_from_directory(
            ".",
            "kitchen.html"
        )

    @app.get("/manager")
    def manager_page():
        return send_from_directory(
            ".",
            "manager.html"
        )

    @app.get("/style.css")
    def stylesheet():
        return send_from_directory(
            ".",
            "style.css"
        )

    @app.get("/logo.png")
    def logo():
        return send_from_directory(
            ".",
            "logo.png"
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": "Bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Resource not found"
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        app.logger.exception(error)

        return jsonify({
            "error": "Internal server error"
        }), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        debug=app.config["DEBUG"]
    )