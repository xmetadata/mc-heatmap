# -*- coding: UTF-8 -*-
import json
from marshmallow import Schema, fields, post_load

from common.utils import CRUD, db, get_uuid

class PropertyModel(db.Model, CRUD):
    __tablename__ = "t_property_dict"
    __table_args__ = {
        'mysql_charset': 'utf8'
    }

    property_uuid = db.Column(db.String(32), default = get_uuid, primary_key = True, comment = '房产类型索引')
    property_name = db.Column(db.String(64), comment = '房产类型名, example: 别墅')
    property_type = db.Column(db.Integer,    comment = '房产类型所属类型, 0: 内置, 1: 自定义')

    def __init__(self, property_name, property_type = 1):
        self.property_name = property_name
        self.property_type = property_type

    @classmethod
    def GetInfo4Dict(cls):
        result = cls.query.all()
        return json.dumps(result)


class PropertySchema(Schema):
    property_uuid = fields.String(required = True)
    property_name = fields.String(required = True)
    property_type = fields.Integer( required = True)