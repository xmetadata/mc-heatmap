# -*- coding: UTF-8 -*-
from marshmallow import Schema, fields, post_load

from common.utils import CRUD, db, get_uuid
from city_dict import CitySchema

class DistrictModel(db.Model, CRUD):
    __tablename__ = "t_district_dict"

    uuid = db.Column(db.String(32), default = get_uuid, primary_key = True, comment = '区域索引')
    district_name = db.Column(db.String(32), comment = '区域名称')
    district_range = db.Column(db.String(128), comment = '区域范围, 用于表示区域范围')
    district_type = db.Column(db.Integer, comment = '区域类型, 0: 内置, 1: 自定义')

    city_uuid = db.Column(db.String(32), db.ForeignKey('t_city_dict.uuid'), comment = '外键，区域所属市索引')
    city = db.relationship('CityModel', backref = db.backref('districts', lazy = 'dynamic'))

    def __init__(self, district_name, district_range, district_type, city):
        self.district_name = district_name
        self.district_range = self.district_range
        self.district_type = district_type
        self.city = city

    @classmethod
    def GetInfo(cls, uuid):
        return cls.query.filter_by(city_uuid = uuid).all()

    @classmethod
    def GetAllInfo():
        return cls.query.all()

class DistrictSchema(Schema):
    uuid = fields.String(required = True)
    district_name = db.String(required = True)
    district_range = db.String(required = True)
    district_type = db.Integer(required = True);
    city = fields.Nested(CitySchema)
