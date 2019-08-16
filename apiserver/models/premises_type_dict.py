# -*- coding: UTF-8 -*-
from marshmallow import Schema, fields, post_load

from common.utils import CRUD, db, get_uuid

class PremisesTypeModel(db.Model, CRUD):
    __tablename__ = "t_premisestype_dict"

    uuid = db.Column(db.String(32), default = get_uuid, primary_key = True, comment = '房产类型索引')
    premisestype_name = db.Column(db.String(64), comment = '房产类型名, example: 别墅')
    premisestype_type = db.Column(db.Integer, comment = '房产类型所属类型, 0: 内置, 1: 自定义')

    def __init__(self, premisestype_name, premisestype_type):
        self.premisestype_name = premisestype_name
        self.premisestype_type = premisestype_type

    @classmethod
    def GetAllInfo(cls):
        cls.query.all()


class PremisesTypeSchema(Schema):
    uuid = fields.String(required = True)
    premisestype_name = fields.String(required = True)
    premisestype_type = fields.Integer( required = True)