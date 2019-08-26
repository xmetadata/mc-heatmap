# -*- coding: UTF-8 -*-
from marshmallow import Schema, fields, post_load
import json
from common.utils import CRUD, db, get_uuid

class ProvinceModel(db.Model, CRUD):
    __tablename__ = "t_province_dict"
    __table_args__ = {
        'mysql_charset': 'utf8'
    }

    province_uuid = db.Column(db.String(36), default = get_uuid, primary_key = True, comment = u'省索引')
    province_name = db.Column(db.String(128), comment = u'省名称')
    province_type = db.Column(db.String(32), default = u'西北', comment = u'省所属区域')

    def __init__(self, province_name, province_type = u'西北'):
        self.province_name = province_name
        self.province_type = province_type

    @classmethod
    def GetInfo4Dict(cls):
        result = cls.query.all()
        return json.dumps(result)


class ProvinceSchema(Schema):
    uuid = fields.String()
    privince_name = fields.String()
