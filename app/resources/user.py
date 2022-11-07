from flask_restful import Resource, reqparse
from app.models.user_model import UserModel
import hmac
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                get_jwt_identity)

# _ before user means its private
_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                            type=str,
                            required=True,
                            help='username is required!!')
_user_parser.add_argument('password',
                            type=str,
                            required=True,
                            help='password is required!!')

class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data["username"]):
            return {"message": "User with that username already exists"}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User create successfully."}, 201

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.delete_from_db()
        return {"message": "User deleted."}, 200

class UserLogin(Resource):
    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()
        # find user in database
        user = UserModel.find_by_username(username=data["username"])
        # check password
        # This is what 'authenticate()' function used to do in security.py file
        if user and hmac.compare_digest(user.password, data["password"]):
            # create access token
            # identity= is what 'identity()' function used to do in security.py file
            access_token = create_access_token(identity=user.id, fresh=True)
            # create refresh token
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200
        return {"message": "Invalid credentials"}, 401

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200