# -*- coding: UTF-8 -*-
from marshmallow import Schema, fields, post_load

from common.utils import CRUD, db, get_uuid

class ProjectsModel(db.Model, CRUD):
    __tablename__ = "projects"
    __table_args__ = {
        'mysql_charset': 'utf8'
    }

    pro_uuid          = db.Column(db.String(32),  default = get_uuid, primary_key = True, comment = u'楼盘索引')
    pro_name          = db.Column(db.String(512), comment = u'楼盘名称')
    pro_address       = db.Column(db.String(512), comment = u'楼盘地址')
    pro_lng           = db.Column(db.String(128), comment = u'楼盘经度')
    pro_lat           = db.Column(db.String(128), comment = u'楼盘纬度')

class ProjectsSchema(Schema):
    pro_uuid    = db.String()
    pro_name    = db.String()
    pro_address = db.String()
    pro_lng     = db.String()
    pro_lat     = db.String()