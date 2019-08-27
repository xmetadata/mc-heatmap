# -*- coding: UTF-8 -*-
import json
import requests
from project_utils import logger, db_exec, db_query, get_uuid
from task_config import PROJECT_DETAILS

class HouseTypeCache:
    def __init__(self):
        self.housetype_map__ = {}
        self.__GenerateDict()

    def __LoadHourse(self):
        sql = "select housetype_uuid, spider_map from t_housingtype_dict"
        try:
            result = db_query(sql)
        except Exception, e:
            logger.error("HouseTypeCache::__LoadHourse: load housetype infomation unsuccessfully.")
            return None
        return result

    def __GenerateDict(self):
        result = self.__LoadHourse()
        if not result:
            return
        for itr in result:
            self.housetype_map__[itr[1]] = itr[0]

    def GetHouseTypeMap(self):
        if len(self.housetype_map__) == 0:
            return None
        return self.housetype_map__

class ProjectSync:
    def __init__(self):
        self.config__         = PROJECT_DETAILS
        self.project_list__   = self.__LoadProject()
        self.housetype_map__  = HouseTypeCache()
        self.sql_value_list__ = []

    def __GenerateHeader(self):
        cookie = db_query("select opt_value from t_options_data where opt_key='cookie'", fetchone=True)
        if not cookie:
            logger.error("ProjectTask::GenerateHeader [ " + self.project_name__ + \
                         "]: Export valid cookie.")
            return None
        self.config__['url_header']['Cookie'] = cookie[0]
        return self.config__['url_header']

    def __GeneratePayload(self, pro_name, house_type):
        payload = self.config__['url_payload']
        payload['sTypeName'] = pro_name
        payload['sRoomTypeIds'] = house_type
        return payload

    def ParseRespon(self, respon):
        try:
            project_num = 0
            header = self.__GenerateHeader()
            for itr in self.project_list__:
                for key, value in self.housetype_map__:
                    payload = self.__GeneratePayload(itr[1], key)
                    try:
                        response = requests.post(self.config__['statistic_url'],
                                                 data={'jsonParameters': json.dumps(payload)}, headers=header)
                    except Exception, e:
                        logger.error("ProjectTask::ParseRespon: request url unsuccessfully, errmsg: " + e.message)
                        continue
                    self.__ParseOneProject(itr[0], value, response)
        except Exception, e:
            logger.error('ProjectSync::ParseRespon: parse response unsuccessfully.')
            return 0
        return project_num

    def ProcessResult(self):
        final_sql = self.__GenerateSql()
        try:
            db_exec(final_sql)
        except Exception, e:
            logger.error('ProjectSync::DealResult: process sql unsuccessfully, sql: ' + final_sql)

    def __LoadProject(self):
        sql = "select pro_uuid, pro_name from t_project_info_data"
        try:
            result = db_query(sql)
        except Exception, e:
            logger.error("ProjectSync::__LoadProject: load projects unsuccessfully.")
            return None
        return result

    def __LoadDistrict(self):
        return None

    def __LoadProperty(self):
        property = db_query("select property_uuid, property_name from t_property_dict")
        if not property:
            logger.error("ProjectSync::__LoadProperty: load property dict unsuccessfully.")
            return
        for itr in property:
            self.property_map__[itr[1]] = itr[0]

    def __ParseOneProject(self, pro_uuid, housetype_uuid, project):
        detail = self.__ResponSerial(project)
        if detail is None or getattr(detail, 'result'):
            return
        detail_uuid = "'%s'" %(get_uuid())
        detail_project_uuid = "'%s'" %(pro_uuid)
        detail_housetype_uuid = "'%s'" %(housetype_uuid)
        detail_area = float(detail['fOneRoomArea'])
        detail_price = float(detail['12580'])
        project_addr = detail['sDistrictName']
        detail_item = "(%s, %s, %s, %f, %f)" \
                % (detail_uuid, detail_project_uuid, detail_housetype_uuid, detail_area, detail_price)
        self.sql_value_list__.append(detail_item)

    def __GenerateSql(self):
        if not len(self.sql_value_list__):
            logger.error("ProjectSync::__GenerateSql: invalid project list.")
            return None
        sql = "insert into t_project_detail_data (detail_uuid, detail_project_uuid, detail_housetype_uuid," \
              "detail_area, detail_price) values"
        for itr in self.sql_value_list__:
            sql += itr
            if itr != self.sql_value_list__[-1]:
                sql += ','
        sql += ';'
        return sql

    def __ResponSerial(self, respon):
        try:
            objs = json.loads(respon)
        except Exception, e:
            logger.error("ProjectSync::__ResponSerial: invalid serialization of response, errmsg: " + e.message)
            return None
        return objs

    @classmethod
    def GeneratePayload(cls, config, page, statistic_type):
        payload = config['url_payload']
        payload['sTypeName'] = statistic_type
        payload['iPageIndex'] = page
        return payload
