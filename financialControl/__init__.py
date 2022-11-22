from flask import Flask
from flask_restful import Api
from .routes.user.api.resource import user_api
from .routes.auth.api.resource import auth_api
from flask_restful_swagger import swagger
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Seans-Python-Flask-REST"
        }
    )

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)
    jwt = JWTManager(app)
    CORS(app)
    load_dotenv()
    app.config['JSON_AS_ASCII'] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://jnvgnqqv:aTo0Yykrx9nCmRavmYFsikv_usQtfOen@fanny.db.elephantsql.com/jnvgnqqv"
    # app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://prisma_test:prisma_pass@database-1.ct3gev1bipds.us-east-2.rds.amazonaws.com/testdb"
    db = SQLAlchemy(app)
    ma = Marshmallow(app)
    db.init_app(app)
    ma.init_app(app)
    Api(app, catch_all_404s=True)
    app.url_map.strict_slashes = False
    app.register_blueprint(user_api, url_prefix="/users")
    app.register_blueprint(auth_api)
    
    
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
    return app

