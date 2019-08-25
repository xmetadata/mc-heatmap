# -*- coding: UTF-8 -*-
from marshmallow import Schema, fields, post_load

from common.utils import CRUD, db, get_uuid

class TotalPriceModel(db.Model, CRUD):
    __tablename__ = "t_totalprice_dict"
    __table_args__ = {
        'mysql_charset': 'utf8'
    }

    uuid = db.Column(db.String(32), default = get_uuid, primary_key = True, comment = u'总价索引')
    price_start = db.Column(db.Integer, comment = u'总价开始数')
    price_start = db.Column(db.Integer, comment = u'总价结束数')
    price_type  = db.Column(db.Integer, comment = u'总价类型, 0: 内置， 1: 自定义')

    def __init__(self, price_start, price_end, price_type):
        self.price_start = price_start
        self.price_end = price_end
        self.price_type = price_type

    @classmethod
    def GetAllInfo(cls):
        cls.query.all()

class TotalPriceSchema(Schema):
    uuid = fields.String(required = True)
    price_start = fields.Integer(required = True)
    price_end   = fields.Integer(required = True)
    price_type  = fields.Integer(required = True)
