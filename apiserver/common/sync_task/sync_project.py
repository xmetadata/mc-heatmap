# -*- coding: UTF-8 -*-
import json
import base64
from project_utils import logger, db_exec, db_query, get_uuid

class ProjectSync:
    def __init__(self):
        self.project_list__ = []
        self.district_map__ = {}
        self.__LoadDistrict()

    def ParseRespon(self, respon):
        respon_objs = self.__ResponSerial(respon)
        if not respon_objs:
            logger.error("ProjectSync::ParseRespon: instance response unsuccessfully.")
            return None
        try:
            project_num = respon_objs['Table'][0]['Column1']
            for itr in respon_objs['Table1']:
                self.__ParseOneProject(itr)
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

    def __LoadDistrict(self):
        province = db_query("select province_uuid, province_name from t_province_dict")
        city     = db_query("select city_uuid, city_name from t_city_dict")
        district = db_query("select district_uuid, district_name from t_district_dict")
        if not province or not city or not district:
            logger.error("ProjectSync::__LoadDistrict: load province/city/district unsuccessfully")
            return
        import pdb
        pdb.set_trace()
        for district_itr in district:
            pass#self.district_map__[district_itr[1]] =


    def __ParseOneProject(self, project):
        proterty_name = base64.b64encode(project['sPropertyName'].encode('utf8'))
        companty_name = base64.b64encode(project['sCompanyName'].encode('utf8'))
        root_price    = project['fRoomPrice']
        root_area     = project['fRoomArea']
        project_item = "(%s, %s, %s, %f, %f)"\
                %("'%s'" %(get_uuid()), "'%s'" %(proterty_name) if proterty_name else "''",
                  "'%s'" %(companty_name) if companty_name else "''",
                  root_price if root_price else 0, root_area if root_area else 0)
        self.project_list__.append(project_item)

    def __GenerateSql(self):
        if not len(self.project_list__):
            logger.error("ProjectSync::__GenerateSql: invalid project list.")
            return None
        sql = "insert into t_project_info_data (pro_uuid, pro_name, pro_company, pro_ave_price, pro_total_area) values"
        for itr in self.project_list__:
            sql += itr
            if itr != self.project_list__[-1]:
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
