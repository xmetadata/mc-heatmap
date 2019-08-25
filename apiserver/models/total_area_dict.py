# -*- coding: UTF-8 -*-
from marshmallow import Schema, fields, post_load

from common.utils import CRUD, db, get_uuid

class TotalAreaModel(db.Model, CRUD):
    __tablename__ = "t_totalarea_dict"
    __table_args__ = {
        'mysql_charset': 'utf8'
    }

    uuid = db.Column(db.String(32), default = get_uuid, primary_key = True, comment = '总面积索引')
    area_start = db.Column(db.Integer, comment = '总面积范围起始')
    area_end = db.Column(db.Integer, comment = '总面积范围结束')
    area_type = db.Column(db.Integer, comment = '总面积类型, 0: 内置, 1: 自定义')

    def __init__(self, area_start, area_end, price_type):
        self.area_start = area_start
        self.area_end = area_end
        self.area_type = area_type

    @classmethod
    def GetAllInfo(cls):
        cls.query.all()

class TotalAreaSchema(Schema):
    uuid = fields.String(required = True)
    area_start = fields.Integer(required = True)
    area_end = fields.Integer(required = True)
    area_type = fields.Integer(required = True)
