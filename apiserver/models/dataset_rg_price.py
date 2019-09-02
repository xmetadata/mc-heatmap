# -*- coding: UTF-8 -*-
from marshmallow import Schema, fields, post_load

from common.utils import CRUD, db, get_uuid

class DatasetPriceModel(db.Model, CRUD):
    __tablename__ = "dataset_price"
    __table_args__ = {
        'mysql_charset': 'utf8'
    }
    uuid     = db.Column(db.String(32),  default = get_uuid, primary_key = True, comment = u'价格索引')
    pro_uuid = db.Column(db.String(32), db.ForeignKey('projects.pro_uuid'),  comment = u'外键，关联楼盘信息')
    city     = db.Column(db.String(64), comment = u'所属省市')
    scope    = db.Column(db.String(64), comment = u'所属区域')
    catalog  = db.Column(db.String(32), comment = u'统计分类')
    stattype = db.Column(db.String(32), comment = u'统计类型')
    statdate = db.Column(db.DateTime,   comment = u'统计日期')
    datetype = db.Column(db.String(32), comment = u'日期类型')
    property = db.Column(db.String(32), comment = u'物业类型')
    arrange  = db.Column(db.String(32), comment = u'排序类型')
    interval = db.Column(db.Integer, default = 0, comment = u'区间标记')
    area     = db.Column(db.Float, default = 0, comment = u'面积')
    number   = db.Column(db.Float, default = 0, comment = u'数量')
    amount   = db.Column(db.Float, comment = u'统计数值')

class DatasetPriceSchema(Schema):
    uuid     = fields.String()
    city     = fields.String()
    scope    = fields.String()
    catalog  = fields.String()
    stattype = fields.String()
    statdate = fields.DateTime(format='%Y-%m-%d')
    datetype = fields.String()
    property = fields.String()
    arrange  = fields.String()
    interval = fields.String()
    area     = fields.Float()
    number   = fields.Float()
    amount   = fields.Float()