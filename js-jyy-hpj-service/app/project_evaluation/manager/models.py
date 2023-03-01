from app import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash


class User(UserMixin, db.Document):

    user_name = db.StringField(required=True, unique=True)

    password_hash = db.StringField(required=True)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Project(db.Document):

    wbs_code = db.StringField(required=True, unique=True)

    name = db.StringField(required=True)

    voltage_level = db.IntField(required=True)

    classification = db.StringField(required=True)

    operation_year = db.IntField(required=True)

    plan_year = db.IntField()

    company_province = db.StringField()

    company_city = db.StringField()

    company_county = db.StringField()

    company = db.StringField(required=True)

    energy_type = db.StringField()

    channel_type = db.StringField()

    budget = db.FloatField()

    capacitance = db.FloatField()

    wire_length = db.FloatField()

    transmission_capacity = db.FloatField()

    def generate_company(self):
        if self.company_city:
            self.company = self.company_city

        self.company = self.company_province


class ProjectDetail(db.DynamicDocument):
    wbs_code = db.StringField(required=True, unique=True)


class ProjectComponent(db.DynamicDocument):
    wbs_code = db.StringField(required=True)
    name = db.StringField(required=True)

# class ProjectEvaluation(db.Document):


class Target(db.Document):
    wbs_code = db.StringField(required=True)
    name = db.StringField(required=True)
    component_name = db.StringField()
    year = db.IntField()
    value = db.FloatField(required=True)
    data_raw = db.DynamicField(required=True)

    status = db.DynamicField()

    average = db.FloatField()
    value_list = db.DynamicField()
    average_list = db.DynamicField()

    def set_status(self, target_status):
        self.status = {
            "color": target_status.color,
            "message": target_status.message
        }

    def __str__(self):
        return "name: %s \n value: %s \n status: %s\n" % (self.name, self.value, self.status) + \
            "year: %s \n average: %s\n " % (self.year, self.average,) + \
            "value_list: %s\n average_list:%s\n" % (self.value_list, self.average_list)


class TargetStatus:

    def __init__(self, color, message):
        self.color = color
        self.message = message
