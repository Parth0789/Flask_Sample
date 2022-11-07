from flask import Flask, Blueprint, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

# from .security import authenticate, identity

from .resources.user import UserRegister, User, UserLogin, TokenRefresh
from app.resources.Item import Item, ItemsList
from app.resources.store import Store, StoreList

from datetime import timedelta
from .Config import database_path

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{database_path}'
app.config["PROPAGATE_EXCEPTIONS"] = True # handle JWT autherisation error and custom errors
# app.config['JWT_AUTH_URL_RULE'] = '/v1/base/login' # Change /auth to custom endpoint

# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

# config JWT auth key name to be 'email' instead of default 'username'
app.config['JWT_AUTH_USERNAME_KEY'] = 'username'


app.secret_key = "parth"
# app.config["JWT_SECRET_KEY"] = "" # key for encoding the jwt token

v1 = Blueprint("v1", __name__, url_prefix="/v1")
base = Blueprint("base", __name__, url_prefix="/base")

api = Api(base)


# jwt = JWT(app, authenticate, identity) #/v1/base/login
jwt = JWTManager(app) #not creating /auth or /login or /v1/base/login

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: # Instead of hard-coding, you should read from a config file or a database
        return {"is_admin": True}
    return {"is_admin": False}

@jwt.expired_token_loader
def expired_token_callback():
    return {"description": "The token has expired.",
            "error": "token_expired"}, 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {"description": "Signature verification failed.",
            "error": "invalid_token"}, 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return {"description": "Request does not contain an access token",
            "error": "authorization_required"}, 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(header, data):
    return {"description": "The token is not fresh.",
            "error": "fresh_token_required"}, 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return {"description": "The token has been revoked.",
            "error": "token_revoked"}, 401


#API End Points
api.add_resource(Store, "/store/<string:name>")
api.add_resource(Item, "/item/<string:name>")

api.add_resource(ItemsList, "/items")
api.add_resource(StoreList, "/stores")

api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")



# Register blueprint
v1.register_blueprint(base)
app.register_blueprint(v1)