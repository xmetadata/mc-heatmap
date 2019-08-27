# -*- coding: UTF-8 -*-
from marshmallow import Schema, fields, post_load

from common.utils import CRUD, db, get_uuid

class HousingTypeModel(db.Model, CRUD):
    __tablename__ = "t_housingtype_dict"
    __table_args__ = {
        'mysql_charset': 'utf8'
    }

    housetype_uuid = db.Column(db.String(36), primary_key = True, comment = u'房屋类型索引')
    housetype_name = db.Column(db.String(64), comment = u'类型名, example: 两室一厅')
    housetype_type = db.Column(db.Integer, comment = u'房屋类型所属类型, 0: 内置, 1:自定义')

    def __init__(self, housetype_name, housetype_type):
        self.housetype_name = housetype_name
        self.housetype_type = housetype_type

    @classmethod
    def GetAllInfo(cls):
        cls.query.all()

class HousingTypeSchema(Schema):
    housetype_uuid = fields.String(required = True)
    housetype_name = fields.String(required = True)
    houdetype_type = fields.String(required = True)
