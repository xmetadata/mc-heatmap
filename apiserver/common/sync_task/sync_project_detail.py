# -*- coding: UTF-8 -*-
import json
import urllib
from project_utils import logger, db_exec, db_query, get_uuid

class ProjectDetailSync:
    def __init__(self):
        self.project_list__ = []

    def ParseRespon(self, respon, config):
        respon_objs = self.__ResponSerial(respon)
        if not respon_objs:
            logger.error("ProjectDetailSync::ParseRespon: instance response unsuccessfully.")
            return None
        try:
            num_of_one_page = int(config['urlParams']['pageCount'])
            project_num = int(respon_objs['totalCount'])
            for itr in respon_objs['Table']:
                self.__ParseOneProject(itr)
        except Exception, e:
            logger.error('ProjectSync::ParseRespon: parse response unsuccessfully, errmsg: ' + e.message)
            return 0
        if project_num%num_of_one_page != 0:
            return int(project_num/num_of_one_page) + 1
        return int(project_num/num_of_one_page)

    def ProcessResult(self):
        final_sql = self.__GenerateSql()
        try:
            db_exec(final_sql)
        except Exception, e:
            logger.error('ProjectSync::DealResult: process sql unsuccessfully, sql: ' + final_sql)

    def __GetDictrict(self, dist):
        city     = db_query("select city_uuid, city_name, province_uuid from t_city_dict")
        if not city:
            logger.error("ProjectDetailSync::__GetDictistic: load province/city/district unsuccessfully")
            return None
        city_dict = {}
        for ctr in city:
            city_dict[ctr[0]] = ctr[2]
        district = db_query("select district_uuid, district_name, city_uuid from t_district_dict")
        if not district:
            logger.error("ProjectDetailSync::__GetDictrict: search district [" + district + "] unsuccessfully.")
            return None
        district_uuid = None
        city_uuid = None
        province_uuid = None
        for dtr in district:
            if dist in dtr[1]:
                district_uuid = dtr[0]
                city_uuid     = dtr[2]
                province_uuid = city_dict[city_uuid]
                break
        if not district_uuid or not province_uuid or not city_uuid:
            logger.error("ProjectDetailSync::__GetDictrict: invalid province/city/district uuid.")
            return None
        return [province_uuid, city_uuid, district_uuid]

    def __ParseOneProject(self, project):
        pro_uuid       = "'%s'" %(get_uuid())
        pro_name       = "'%s'" %(project['title'])
        pro_address    = "'%s'" %(project['address'])
        pro_company    = "'%s'" %(project['developer'])
        pro_ave_price  = float(project['price_num'])
        pro_sale_card  = "'%s'" %(project['sSaleCard'])
        pro_total_area = float(project['fGroundArea'])
        pro_total_door = int(project['sTotalDoor'])
        pro_lng        = str(project['x'])
        pro_lat        = str(project['y'])
        pro_sale_date  = "'%s'" % (project['openDate'])
        province_uuid = "'%s'" % (u'db448841c7a011e9878e00163e1caaa2')
        city_uuid     = "'%s'" % (u'db448840c7a011e9878e00163e1caaa2')
        district_uuid = "'%s'" % (u'db448851c7a011e9878e00163e1caaa2')
        project_item = "(%s, %s, %s, %s, %f, %s, %f, %d, %s, %s, %s, %s, %s, %s)"\
                %(pro_uuid, pro_name, pro_address, pro_company, pro_ave_price, pro_sale_card, pro_total_area,
                  pro_total_door, pro_lng, pro_lat, pro_sale_date, province_uuid, city_uuid, district_uuid)
        self.project_list__.append(project_item)

    def __ResponSerial(self, respon):
        try:
            objs = json.loads(respon)
        except Exception, e:
            logger.error("ProjectDetailSync::__ResponSerial: invalid serialization of response, errmsg: " + e.message)
            return None
        return objs

    def __GenerateSql(self):
        if not len(self.project_list__):
            logger.error("ProjectDetailSync::__GenerateSql: invalid project list.")
            return None
        sql = "insert into t_project_info_data (pro_uuid, pro_name, pro_address, pro_company, pro_ave_price, pro_sale_card," \
              "pro_total_area, pro_total_door, pro_lng, pro_lat, pro_sale_date, pro_province_uuid, pro_city_uuid, pro_district_uuid) values"
        for itr in self.project_list__:
            sql += itr
            if itr != self.project_list__[-1]:
                sql += ','
        sql += ';'
        return sql

    @classmethod
    def GeneratePayload(cls, config, page, statistic_type):
        payload = config['url_payload']
        payload['type'] = statistic_type
        payload['urlParams']['iPageIndex'] = page
        return payload
