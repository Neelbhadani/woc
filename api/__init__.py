import os
from flask import Flask
from api.extensions import mongo, mail


def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb+srv://woc:<db_password>@cluster0.ujqjf85.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    app.config["BASE_URL"] = os.getenv("BASE_URL")

    mongo.init_app(app)
    mail.init_app(app)

    from api.route import user_bp
    app.register_blueprint(user_bp, url_prefix='/api')

    return app

