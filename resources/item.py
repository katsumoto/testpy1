# from flask import Flask, request
# from flask_restful import Resource, Api,reqparse
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type = float,required = True,help = "not to be blank")
    parser.add_argument("stores_id", type = int,required = True,help = "Store id is needed")

    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return {"item" : item.json()}

        return {"message" : "item not found"}, 404

    def post(self,name):
        try:
            if ItemModel.find_by_name(name):
                return {"message" : "item {} already exists".format(name) }, 400
        except:
            return {"message" : "find by name failed"}, 500

        data = Item.parser.parse_args()
        item = ItemModel(name, data["price"], data["stores_id"])
        try:
            item.save_to_db()
        except:
                return {"messsage" : "insert failed"}, 500
        return item.json(),201

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message" : "item deleted"}
        else:
            return {"message" : "item not found"}


    def put(self,name):
        data = Item.parser.parse_args()
        try:
            item = ItemModel.find_by_name(name)
        except:
                return {"message" : "find by name failed"}, 500

        if item is None:
            item = ItemModel(name, data["price"], data["stores_id"])
        else:
            item.price = data["price"]
            item.stores_id = data["stores_id"]

        item.save_to_db()
        return {"item" : item.json()}


class ItemList(Resource):
    def get(self):
        allItems = ItemModel.query.all()
        res = []
        for item in allItems:
            res.append(item.json())

        return {"items" : res}
