# -*- coding: UTF-8 -*-
import json
from urllib import urlencode
from project_utils import logger
from project_utils import db_query, db_exec

class ProjectSync:
    def __init__(self):
        self.project_list__ = []
        self.province_map__ = {}
        self.city_map__     = {}
        self.district_map__ = {}

    def ParseRespon(self, respon):
        respon_objs = self.__ResponSerial(respon)
        if not respon_objs:
            logger.error("ProjectSync::ParseRespon: parse response unsuccessfully.")
            return None
        project_num = respon_objs['Table'][0]['Column1']
        for itr in respon_objs['Table1']:
            ret_status = self.__ParseOneProject(itr)
            if not ret_status:
                logger.warn("ProjectSync::ParseRespon: parse project unsuccessfully, obj: " + json.dumps(itr))

    def DealResult(self):
        final_sql = self.__GenerateSql()
        db_exec(final_sql, executemany=True)

    def __ParseOneProject(self, project):
        project_item = "(%s, %s, %f, %f)"\
                %(project['sPropertyName'], project['sCompanyName'], project['fRoomPrice'], project['fRoomArea'])
        self.project_list__.append(project_item)

    def __GenerateSql(self):
        if len(self.project_list__):
            logger.error("ProjectSync::__GenerateSql: invalid project list.")
            return None
        sql = "insert into t_projectinfo_data ('pro_name', 'pro_company', 'pro_ave_price', 'pro_total_area') values"
        for itr in self.project_list__:
            sql += itr
            if itr != self.project_list__[-1]:
                sql += ','
        return sql

    def __ResponSerial(self, respon):
        try:
            objs = json.loads(respon)
        except Exception, e:
            logger.error("ProjectSync::__ResponSerial: invalid serialization of response, errmsg: " + e.message)
            return None
        return objs
