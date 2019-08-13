# -*- coding: UTF-8 -*-
from marshmallow import Schema, fields, post_load

from common.utils import CRUD, db, get_uuid

class HousingTypeModel(db.Model, CRUD):
    __tablename__ = "t_housingtype_dict"

    uuid = db.Column(db.String(32), primary_key = True, comment = '房屋类型索引')
    housetype_name = db.Column(db.String(64), comment = '类型名, example: 两室一厅')
    housetype_type = db.Column(db.Integer, comment = '房屋类型所属类型, 0: 内置, 1:自定义')

    def __init__(self, housetype_name, housetype_type):
        self.housetype_name = housetype_name
        self.housetype_type = housetype_type

    @classmethod
    def GetAllInfo(cls):
        cls.query.all()

class HousingTypeSchema(Schema):
    uuid = fields.String(required = True)
    housetype_name = fields.String(required = True)
    houdetype_type = fields.String(required = True)
