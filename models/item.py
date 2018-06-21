from db import db

class ItemModel(db.Model):
    #alchemy
    __tablename__ = "items"
    id =  db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))
    price = db.Column(db.Float(precision=2))
    stores_id = db.Column(db.Integer,db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")

    def __init__(self,name, price, stores_id):
        self.name = name;
        self.price = price
        self.stores_id = stores_id

    def json(self):
        return {"name" : self.name, "price" : self.price, "stores_id" : self.stores_id}

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name = name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
