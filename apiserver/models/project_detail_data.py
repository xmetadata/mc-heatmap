# -*- coding: UTF-8 -*-
from marshmallow import Schema, fields, post_load

from common.utils import CRUD, db, get_uuid
from project_infomation_data import ProjectInfomationSchema

class ProjectDetailModel(db.Model, CRUD):
    __tablename__ = "t_projectdetail_data"

    uuid           = db.Column(db.String(32), default = get_uuid, primary_key = True, comment = '楼盘详情索引')
    statistic_date = db.Column(db.String(32), default = get_uuid, primary_key = True, comment = '数据统计日期')
    housingtype_
