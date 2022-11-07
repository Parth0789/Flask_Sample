from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required,
                                get_jwt,
                                get_jwt_identity)
from app.models.item_model import ItemModel
#API Resources
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='Price cannot be empty!'
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='StroeID cannot be empty!')
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {"message": "Item not found"}, 404

    @jwt_required(fresh=True)
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()
        item =ItemModel(name, data["price"], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}
        return item.json(), 201 # 201 status code for created

    @jwt_required()
    def delete(self, name):
        claims = get_jwt()
        print(claims)
        if not claims["is_admin"]:
            return {"message": "Admin privilege required."}, 401
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name) # The item is not found in the database
        if item:
            try:
                item.price = data['price']
            except:
                return {"message": "An error occurred updating the item"}, 500
        else:
            try:

                item = ItemModel(name, data['price'], data['store_id'])
            except:
                return {"message": "An error occurred inserting the item"}, 500  # 500 internal server error

        item.save_to_db()
        return item.json()


class ItemsList(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        items = ItemModel.get_all_items()
        if user_id:
            return {"items": items}, 200
        return {
            "items": [item["name"] for item in items],
            "message": "More data available if you log in."
        }, 200