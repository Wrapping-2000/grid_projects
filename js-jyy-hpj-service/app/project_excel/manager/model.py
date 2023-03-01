from app import db


class Excel(db.Document):
    name = db.StringField(required=True)
    file = db.DictField(required=True)
