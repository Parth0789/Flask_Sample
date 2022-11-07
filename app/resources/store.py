from flask_restful import Resource, reqparse
from app.models.store_model import StoreModel

class Store(Resource):
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

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {"message": "Store not found"}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {"message": "A Store with name '{}' already exists".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred with creating the store"}, 500
        return store.json()

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": "Store deleted"}


class StoreList(Resource):
    def get(self):
        return {"stores": StoreModel.get_all_stores()}