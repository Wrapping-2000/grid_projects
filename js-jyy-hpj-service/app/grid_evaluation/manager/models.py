from app import db


class GenerateCapacity(db.Document):
    name = db.StringField(required=True)
    amount = db.FloatField(required=True)
    unit = db.StringField(required=True)
    date = db.StringField(required=True)


class SocialPowerAndLoadValue(db.Document):
    name = db.StringField(required=True)
    amount = db.FloatField(required=True)
    unit = db.StringField(required=True)
    date = db.StringField(required=True)


class VoltageLevel(db.Document):
    name = db.StringField(required=True)
    date = db.StringField(required=True)
    length = db.FloatField(required=True)
    line_num = db.IntField(required=True)
    substation_num = db.IntField(required=True)


class InstallCapacity(db.Document):
    name = db.StringField(required=True)
    amount = db.FloatField(required=True)
    unit = db.StringField(required=True)
    date = db.StringField(required=True)


class VariableCapacity(db.Document):
    name = db.StringField(required=True)
    amount = db.FloatField(required=True)
    unit = db.StringField(required=True)
    date = db.StringField(required=True)


class HouseNumber(db.Document):
    low_level = db.IntField(required=True)
    low_level_not = db.IntField(required=True)
    high_level = db.IntField(required=True)
    date = db.StringField(required=True)