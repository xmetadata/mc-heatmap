# -*- coding: UTF-8 -*-
from marshmallow import Schema, fields, post_load
from common.utils import CRUD, db, get_uuid

class ProjectDetailModel(db.Model, CRUD):
    __tablename__ = 't_project_detail_data'
    __table_args__ = {
        'mysql_charset': 'utf8'
    }
    detail_uuid = db.Column(db.String(32), default = get_uuid, primary_key = True, comment = u'楼盘详情索引')
    pass


class ProjectDetailSchema(Schema):
    detail_uuid = fields.String()
    pass