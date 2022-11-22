from flask import Flask
from flask_restful import Api
from .routes.user.api.resource import user_api
from .routes.auth.api.resource import auth_api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from flasgger import Swagger

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)
    CORS(app)
    load_dotenv()
    app.config['JSON_AS_ASCII'] = False
    app.config['JWT_SECRET_KEY'] = "8f42a73054b1749f8f58848be5e6502c"
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
    swagger_template = {
        "info": {
            'title': 'Financial Control Prisma',
            'version': '1.0.0',
            'description': 'Technical test. Prisma has considered developing an expense management and control system to help its employees control their monthly budget. control system so that they can control their monthly budget. For this purpose, it is requested to develop the Back-end layer services using the necessary technologies. You must enter in authorize the Bearer token that is returned in the login endpoint.',
        },
        "host": "test-prisma-v1.herokuapp.com",
        "schemes":["https"],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Authorization: Bearer {token}"
            }   
        },
        "security": [
            {
                "Bearer": []
            }
        ]
    }
    swagger = Swagger(app, template=swagger_template)
    return app

