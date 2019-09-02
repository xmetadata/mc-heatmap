# -*- coding: UTF-8 -*-
from marshmallow import Schema, fields, post_load

from common.utils import CRUD, db, get_uuid
from models.dataset_rg_room import DatasetRoomModel, DatasetRoomSchema
from models.dataset_rg_area import DatasetAreaModel, DatasetAreaSchema
from models.dataset_rg_amount import DatasetAmountModel, DatasetAmountSchema
from models.dataset_rg_none import DatasetNoneModel, DatasetNoneSchema
from models.dataset_rg_price import DatasetPriceModel, DatasetPriceSchema

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
    dataset_room      = db.relationship('DatasetRoomModel', backref = db.backref('project'),    lazy = 'dynamic')
    dataset_area      = db.relationship('DatasetAreaModel', backref = db.backref('project'), lazy = 'dynamic')
    dataset_amount    = db.relationship('DatasetAmountModel', backref=db.backref('project'), lazy='dynamic')
    dataset_none      = db.relationship('DatasetNoneModel', backref=db.backref('project'), lazy='dynamic')
    dataset_price     = db.relationship('DatasetPriceModel', backref=db.backref('project'), lazy='dynamic')

class ProjectsSchema(Schema):
    pro_uuid    = fields.String()
    pro_name    = fields.String()
    pro_address = fields.String()
    pro_lng     = fields.String()
    pro_lat     = fields.String()
    dataset_room = fields.Nested(DatasetRoomSchema)
    dataset_area = fields.Nested(DatasetAreaSchema)
    dataset_amount = fields.Nested(DatasetAmountSchema)
    dataset_none = fields.Nested(DatasetNoneSchema)
    dataset_price = fields.Nested(DatasetPriceSchema)