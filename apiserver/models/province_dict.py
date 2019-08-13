# -*- coding: UTF-8 -*-
from marshmallow import Schema, fields, post_load

from common.utils import CRUD, db, get_uuid

class ProvinceModel(db.Model, CRUD):
    __tablename__ = "t_province_dict"
    
    uuid = db.Column(db.String(32), default = get_uuid, primary_key = True, comment = '省索引')
    privince_name = db.Column(db.String(128), comment = '省名称')
    privince_type = db.Column(dh.String(32), default = "西北", comment = '省所属区域')

    def __init__(self, privince_name):
        self.privince_name = privince_name
        self.privince_type = privince_type

    @classmethod
    def GetAllInfo(cls):
        return cls.query.all()


class ProvinceSchema(Schema):
    uuid = fields.String(required = True)
    privince_name = fields.String(required = True)
