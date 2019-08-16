# -*- coding: UTF-8 -*-
from marshmallow import Schema, fields, post_load

from common.utils import CRUD, db, get_uuid
from province_dict import ProvinceSchema
from city_dict import CitySchema
from district_dict import DistrictSchema

class ProjectInfomationModel(db.Model, CRUD):
    __tablename__ = "t_projectinfo_data"

    uuid = db.Column(db.String(32), default = get_uuid, primary_key = True, comment = '楼盘索引')
    statistic_date    = db.Column(db.DateTime, comment = '数据统计日期')
    project_name      = db.Column(db.String(128), comment = '楼盘名称')
    pro_lng           = db.Column(db.Float, comment = '楼盘所在经度')
    pro_lat           = db.Column(db.Float, comment = '楼盘所在纬度')
    pro_price         = db.Column(db.Float, comment = '楼盘均价')
    pro_total_area    = db.Column(db.Float, comment = '楼盘上市总面积')
    pro_area_sold     = db.Column(db.Float, comment = '楼盘已售面积')
    pro_area_selling  = db.Column(db.Float, comment = '楼盘在售面积')
    pro_tatol_num     = db.Column(db.Integer, comment = '楼盘上市总套数')
    pro_sold_num      = db.Column(db.Integer, comment = '楼盘已售套数')
    pro_selling_num   = db.Column(db.Integer, comment = '楼盘在售套数')

    province_uuid     = db.Column(db.String(32), db.ForeignKey('t_province_dict.uuid'), comment = '外键, 关联省份')
    province          = db.relationship('ProvinceModel', backref = db.backref('houses'), lazy = 'dynamic')
    city_uuid         = db.Column(db.String(32), db.ForeignKey('t_city_dict.uuid'), comment = '外键, 关联城市')
    city              = db.relationship('CityModel', backref = db.backref('houses'), lazy = 'dynamic')
    district_uuid     = db.Column(db.String(32), db.ForeignKey('t_district_dict.uuid'), comment = '外键, 关联城市行政区')
    district          = db.relationship('DistrictModel', backref = db.backref('houses'), lazy = 'dynamic')
    
