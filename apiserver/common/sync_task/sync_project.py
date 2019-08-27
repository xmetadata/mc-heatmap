# -*- coding: UTF-8 -*-
import json
from project_utils import logger, db_exec, db_query

class ProjectSync:
    def __init__(self):
        self.project_list__ = []

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

    def __LoadProject(self):
        sql = "select "

    def __LoadDistrict(self):
        city     = db_query("select city_uuid, city_name, province_uuid from t_city_dict")
        district = db_query("select district_uuid, district_name, city_uuid from t_district_dict")
        if not city or not district:
            logger.error("ProjectSync::__LoadDistrict: load province/city/district unsuccessfully")
            return
        city_dict = {}
        for ctr in city:
            city_dict[ctr[0]] = ctr[2]
        for itr in district:
            value = [city_dict[itr[2]], itr[2], itr[0]]
            self.district_map__[itr[1]] = value

    def __LoadProperty(self):
        property = db_query("select property_uuid, property_name from t_property_dict")
        if not property:
            logger.error("ProjectSync::__LoadProperty: load property dict unsuccessfully.")
            return
        for itr in property:
            self.property_map__[itr[1]] = itr[0]

    def __ParseOneProject(self, project):
        project_uuid  = project['sPropertyID']
        proterty_name = project['sPropertyName']
        companty_name = project['sCompanyName']
        root_price    = project['fRoomPrice']
        root_area     = project['fRoomArea']
        property_attr = self.district_map__[project['sDistrictName']]  if self.district_map__.get(project['sDistrictName']) else None
        province_uuid = "'%s'" %(property_attr[0]) if property_attr else "''"
        city_uuid     = "'%s'" %(property_attr[1]) if property_attr else "''"
        district_uuid = "'%s'" %(property_attr[2]) if property_attr else "''"

        project_item = "(%s, %s, %s, %f, %f, %s, %s, %s)"\
                %("'%s'" %(project_uuid), "'%s'" %(proterty_name) if proterty_name else "''",
                  "'%s'" %(companty_name) if companty_name else "''",
                  root_price if root_price else 0, root_area if root_area else 0,
                  province_uuid,  city_uuid, district_uuid)
        self.project_list__.append(project_item)

    def __GenerateSql(self):
        if not len(self.project_list__):
            logger.error("ProjectSync::__GenerateSql: invalid project list.")
            return None
        sql = "insert into t_project_info_data (pro_uuid, pro_name, pro_company, pro_ave_price, pro_total_area," \
              "pro_province_uuid, pro_city_uuid, pro_district_uuid) values"
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

    @classmethod
    def GeneratePayload(cls, config, page, statistic_type):
        payload = config['url_payload']
        payload['sTypeName'] = statistic_type
        payload['iPageIndex'] = page
        return payload
