# -*- coding: UTF-8 -*-
from marshmallow import Schema, fields, post_load

from common.utils import CRUD, db, get_uuid
from province_dict import ProvinceSchema
from city_dict import CitySchema
from district_dict import DistrictSchema
from project_property import PropertySchema

class ProjectInfomationModel(db.Model, CRUD):
    __tablename__ = "t_project_info_data"
    __table_args__ = {
        'mysql_charset': 'utf8'
    }

    pro_uuid          = db.Column(db.String(36),  default = get_uuid, primary_key = True, comment = u'楼盘索引')
    pro_name          = db.Column(db.String(512), comment = u'楼盘名称')
    pro_address       = db.Column(db.String(512), comment = u'楼盘地址')
    pro_company       = db.Column(db.String(512), comment = u'楼盘开发商')
    pro_ave_price     = db.Column(db.Float,       comment = u'楼盘平均价格')
    pro_sale_card     = db.Column(db.String(512),  comment = u'楼盘预售证')
    pro_total_door    = db.Column(db.Integer,     comment = u'楼盘总套数')
    pro_sold_door     = db.Column(db.Integer,     comment = u'楼盘已售套数')
    pro_selling_door  = db.Column(db.Integer,     comment = u'楼盘在售套数')
    pro_total_area    = db.Column(db.Float,       comment = u'楼盘总面积')
    pro_sold_area     = db.Column(db.Float,       comment = u'楼盘已售面积')
    pro_selling_area  = db.Column(db.Float,       comment = u'楼盘在售面积')
    pro_lng           = db.Column(db.String(128), comment = u'楼盘经度')
    pro_lat           = db.Column(db.String(128), comment = u'楼盘纬度')
    pro_sale_date     = db.Column(db.DateTime,    comment = u'楼盘开始售卖日期')

    pro_property_uuid = db.Column(db.String(36), db.ForeignKey('t_property_dict.property_uuid'),     comment = u'外键，关联项目类型，住宅，商铺，写字楼')
    pro_property      = db.relationship('PropertyModel', backref = db.backref('projects'),    lazy = 'dynamic')
    pro_province_uuid = db.Column(db.String(36), db.ForeignKey('t_province_dict.province_uuid'),     comment = u'外键，关联楼盘所属省份')
    pro_province      = db.relationship('ProvinceModel', backref = db.backref('projects'),    lazy = 'dynamic')
    pro_city_uuid     = db.Column(db.String(36), db.ForeignKey('t_city_dict.city_uuid'),             comment = u'外键，关联楼盘所属城市')
    pro_city          = db.relationship('CityModel', backref = db.backref('projects'),        lazy = 'dynamic')
    pro_district_uuid = db.Column(db.String(36), db.ForeignKey('t_district_dict.district_uuid'),     comment = u'外键，关联楼盘所属区域')
    pro_district      = db.relationship('DistrictModel', backref = db.backref('projects'),    lazy = 'dynamic')

    #获取所有楼盘
    @classmethod
    def GetInfoAll(cls):
        return cls.query.all()

    #根据省份获取楼盘
    @classmethod
    def GetInfoByProvince(cls):
        pass

    #根据城市获取楼盘
    @classmethod
    def GetInfoByCity(cls):
        pass

    #根据区域获取楼盘
    @classmethod
    def GetInfoByDistrict(cls):
        pass

    #根据平均价获取楼盘
    @classmethod
    def GetInfoByAvePrice(cls, start, end):
        pass

class ProjectInfomationSchema(Schema):
    pro_uuid            = fields.String()
    pro_name            = fields.String()
    pro_address         = fields.String()
    pro_company         = fields.String()
    pro_ave_price       = fields.Float()
    pro_sale_card       = fields.String()
    pro_total_door      = fields.Integer()
    pro_sold_door       = fields.Integer()
    pro_selling_door    = fields.Integer()
    pro_total_area      = fields.Float()
    pro_sold_area       = fields.Float()
    pro_selling_area    = fields.Float()
    pro_lng             = fields.String()
    pro_lat             = fields.String()
    pro_sale_date       = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    pro_property        = fields.Nested(PropertySchema)
    pro_province        = fields.Nested(ProvinceSchema)
    pro_city            = fields.Nested(CitySchema)
    pro_district        = fields.Nested(DistrictSchema)