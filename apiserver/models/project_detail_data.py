# -*- coding: UTF-8 -*-
from marshmallow import Schema, fields, post_load
from common.utils import CRUD, db, get_uuid
from project_infomation_data import ProjectInfomationSchema
from project_property import PropertySchema
from housing_type_dict import HousingTypeSchema

class ProjectDetailModel(db.Model, CRUD):
    __tablename__ = 't_project_detail_data'
    __table_args__ = {
        'mysql_charset': 'utf8'
    }
    detail_uuid           = db.Column(db.String(36), default = get_uuid, primary_key = True, comment = u'楼盘详情索引')
    detail_project_uuid   = db.Column(db.String(36), db.ForeignKey('t_project_info_data.pro_uuid'), comment = u'楼盘索引')
    detail_project        = db.relationship('ProjectInfomationModel', backref = db.backref('projects'),    lazy = 'dynamic')
    detail_property_uuid  = db.Column(db.String(36), db.ForeignKey('t_property_dict.property_uuid'),     comment = u'外键，关联项目类型，住宅，商铺，写字楼')
    detail_property       = db.relationship('PropertyModel', backref = db.backref('projects'),    lazy = 'dynamic')
    detail_housetype_uuid = db.Column(db.String(36), db.ForeignKey('t_housingtype_dict.housetype_uuid'), comment = u'外键，关联房屋属性，一室， 两室...')
    detail_housetype      = db.relationship('HousingTypeModel', backref=db.backref('projects'), lazy='dynamic')
    detail_area           = db.Column(db.Float, comment = u'当前楼盘在该类型下的房屋属性的面积')
    detail_price          = db.Column(db.Float, default = 0, comment = u'当前楼盘在该类型下的房屋属性的价格')

class ProjectDetailSchema(Schema):
    detail_uuid             = fields.String()
    detail_project_uuid     = fields.String()
    detail_project          = fields.Nested(ProjectInfomationSchema)
    detail_property_uuid    = fields.String()
    detail_property         = fields.Nested(PropertySchema)
    detail_housetype_uuid   = fields.String()
    detail_housetype        = fields.Nested(HousingTypeSchema)
    detail_area             = fields.Float()
    detail_price            = fields.Float()
