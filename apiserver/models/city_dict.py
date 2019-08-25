# -*- coding: UTF-8 -*-
from marshmallow import Schema, fields, post_load

from common.utils import CRUD, db, get_uuid
from province_dict import ProvinceSchema

class CityModel(db.Model, CRUD):
    __tablename__ = "t_city_dict"
    __table_args__ = {
        'mysql_charset': 'utf8'
    }

    city_uuid = db.Column(db.String(32), default = get_uuid, primary_key = True, comment = '市索引')
    city_name = db.Column(db.String(32), comment = '市名称')
    city_type = db.Column(db.String(128), default = "地级市", comment = '市类型')

    province_uuid = db.Column(db.String(32), db.ForeignKey('t_province_dict.uuid'), comment = '外键， 关联省字典表')
    province = db.relationship('ProvinceModel', backref = db.backref('citys', lazy = 'dynamic'))

    def __init__(self, city_name, province):
        self.city_name = city_name
        self.privince = province

    @classmethod
    def GetInfo(cls, uuid):
        return cls.query.filter_by(province_uuid = uuid).all()

    @classmethod
    def GetAllInfo(cls):
        return cls.query.all()


class CitySchema(Schema):
    uuid = fields.String()
    city_name = db.String()
    province = fields.Nested(ProvinceSchema)
