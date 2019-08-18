# -*- coding: UTF-8 -*-
import json
from datetime import datetime

from flask import current_app
from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, request
from sqlalchemy.exc import SQLAlchemyError

from common.utils import StandardResponse
from models.project_infomation_data import ProjectInfomationModel, ProjectInfomationSchema

class ProBaseInfo(Resource):
    @jwt_required()
    def get(self, uuid):
        pass

class ProBaseInfoList(Resource):
    @jwt_required()
    def get(self):
        pass