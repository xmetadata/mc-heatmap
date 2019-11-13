# -*- coding: UTF-8 -*-
import json
import copy
from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, request

from common.utils import StandardResponse
from models.projects import ProjectsModel, ProjectsSchema


class ProjectMgr(Resource):
    def __init__(self):
        self.project_page__ = {
            "total": 0,
            "page_index": 1,
            "page_size": 100,
            "list": []
        }
        self.project__ = {
            "name": "",
            "address": "",
            "uuid": "",
            "lng": 0,
            "lat": 0
        }
    @jwt_required()
    def get(self):
        if not request.args.get('_page') or not request.args.get('_limit'):
            return StandardResponse(400, 1, u'Invalid Request Parameters')
        try:
            project_page = copy.deepcopy(self.project_page__)
            project_page["page_index"] = int(request.args.get('_page'))
            project_page["page_size"] = int(request.args.get('_limit'))
            pro_name = request.args.get('pro_name')
            projects = None
            if not pro_name or len(pro_name) == u"":
                project_page["total"] = ProjectsModel.query.count()
                projects = ProjectsModel.query.paginate(
                    project_page["page_index"], per_page=project_page["page_size"], error_out=False)
            else:
                project_page["total"] = ProjectsModel.query.filter(ProjectsModel.pro_name.like('%' + pro_name + '%')).count()
                projects = ProjectsModel.query.filter(ProjectsModel.pro_name.like('%' + pro_name + '%')).paginate(
                    project_page["page_index"], per_page=project_page["page_size"], error_out=False)
            for itr in projects.items:
                project = copy.deepcopy(self.project__)
                project["name"] = itr.pro_name
                project["address"] = itr.pro_address
                project["uuid"] = itr.pro_uuid
                project['lng'] = float(itr.pro_lng) if itr.pro_lng else 0.0
                project['lat'] = float(itr.pro_lat) if itr.pro_lat else 0.0
                project_page["list"].append(project)
        except Exception, e:
            return StandardResponse(500, 1, e.message)
        return StandardResponse(200, 0, data = project_page)

    @jwt_required()
    def put(self):
        req_data = request.get_json()
        if not req_data:
            return StandardResponse(400, 1, u"无效的请求参数")
        if not req_data.has_key("project") or \
           not req_data.has_key("name") or \
           not req_data.has_key("address"):
            return StandardResponse(400, 1, u"无效的请求参数")
        try:
            project = ProjectsModel.query.filter(ProjectsModel.pro_uuid == req_data["project"]).fetchone()
            if not project:
                return StandardResponse(500, 1, u"无法更新目标数据")
            project.pro_name = req_data["name"]
            project.pro_address = req_data["address"]
            project.update()
        except Exception, e:
            return StandardResponse(500, 1, e.message)
        return StandardResponse(200, 0, u"Delete Success")

    @jwt_required()
    def delete(self):
        req_data = request.get_json()
        if not req_data:
            return StandardResponse(400, 1, u"无效的请求参数")
        if not req_data.has_key("project"):
            return StandardResponse(400, 1, u"无效的请求参数")
        try:
            project = ProjectsModel.query.filter(ProjectsModel.pro_uuid == req_data["project"]).fetchone()
            if not project:
                return StandardResponse(500, 1, u"无法更新目标数据")
            project.delete()
        except Exception, e:
            return StandardResponse(500, 1, e.message)
        return StandardResponse(200, 0, u'Update Success')

class ProjectCtl(Resource):
    def __init__(self):
        pass

    @jwt_required()
    def put(self, uuid):
        req_data = request.get_json()
        if not req_data:
            return StandardResponse(400, 1, u"无效的请求参数")
        if not req_data.has_key("uuid") or \
           not req_data.has_key("name") or \
           not req_data.has_key("address") or \
           not req_data.has_key("lat") or \
           not req_data.has_key("lng"):
            return StandardResponse(400, 1, u"无效的请求参数")
        project = ProjectsModel.query.filter(ProjectsModel.pro_uuid == uuid).first()
        if not project:
            return StandardResponse(500, 1, u"无法更新目标数据")
        project.pro_name = req_data["name"]
        project.pro_address = req_data["address"]
        project.pro_lat = req_data["lat"]
        project.pro_lng = req_data["lng"]
        project.update()
        return StandardResponse(200, 0, u"Update Success")

    @jwt_required()
    def delete(self, uuid):
        req_data = request.get_json()
        if not req_data:
            return StandardResponse(400, 1, u"无效的请求参数")
        if not req_data.has_key("project"):
            return StandardResponse(400, 1, u"无效的请求参数")
        project = ProjectsModel.query.filter(ProjectsModel.pro_uuid == req_data["project"]).first()
        if not project:
            return StandardResponse(500, 1, u"无法更新目标数据")
        project.delete()
        return StandardResponse(200, 0, u'Delete Success')
