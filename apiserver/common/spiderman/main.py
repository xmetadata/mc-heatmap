# -*- coding: UTF-8 -*-
import datetime
import difflib
import json
import time

import requests

from config import STATDELTA, STATTYPES
from spider import prepare_statdata, initialize_browser, close_browser
from utils import get_option, set_option, sql_exec, sql_query

if __name__ == "__main__":
    browser = initialize_browser()
    current_datetime = datetime.datetime.now()
    # 统计resume_statdate_month
    statdate = datetime.datetime.strptime(
        get_option("resume_statdate_month"), '%Y-%m-%d')
    delta = current_datetime - statdate
    for item in range(1, delta.days - STATDELTA):
        statdate_item = statdate + datetime.timedelta(days=item)
        if 1 == int(statdate_item.day):  # 月初统计上月月报
            enddate = statdate_item - datetime.timedelta(days=1)
            startdate = datetime.datetime.strptime(
                '%s-%s-%s' % (enddate.year, enddate.month, 1), '%Y-%m-%d')
            for stattype in STATTYPES:
                prepare_statdata(browser, stattype, startdate.strftime(
                    '%Y-%m-%d'), enddate.strftime('%Y-%m-%d'), 'month')
        # 更新统计日期
        set_option("resume_statdate_month", statdate_item.strftime('%Y-%m-%d'))
    # 统计resume_statdate_day
    statdate = datetime.datetime.strptime(
        get_option("resume_statdate_day"), '%Y-%m-%d')
    delta = current_datetime - statdate
    for item in range(1, delta.days - STATDELTA):
        statdate_item = statdate + datetime.timedelta(days=item)
        for stattype in STATTYPES[:-1]:  # 按天不统计 可售情况
            prepare_statdata(browser, stattype, statdate_item.strftime(
                '%Y-%m-%d'), statdate_item.strftime('%Y-%m-%d'), 'day')
        # 更新统计日期
        set_option("resume_statdate_day", statdate_item.strftime('%Y-%m-%d'))
    # 统计arrange_area_statdate
    statdate = datetime.datetime.strptime(
        get_option("arrange_area_statdate"), '%Y-%m-%d')
    delta = current_datetime - statdate
    for item in range(1, delta.days - STATDELTA):
        statdate_item = statdate + datetime.timedelta(days=item)
        if 1 == int(statdate_item.day):  # 月初统计上月月报
            enddate = statdate_item - datetime.timedelta(days=1)
            startdate = datetime.datetime.strptime(
                '%s-%s-%s' % (enddate.year, enddate.month, 1), '%Y-%m-%d')
            for stattype in STATTYPES[:-1]:
                prepare_statdata(browser, stattype, startdate.strftime(
                    '%Y-%m-%d'), enddate.strftime('%Y-%m-%d'), 'month', 'area')
        # 更新统计日期
        set_option("arrange_area_statdate", statdate_item.strftime('%Y-%m-%d'))
    # 统计arrange_room_statdate
    statdate = datetime.datetime.strptime(
        get_option("arrange_room_statdate"), '%Y-%m-%d')
    delta = current_datetime - statdate
    for item in range(1, delta.days - STATDELTA):
        statdate_item = statdate + datetime.timedelta(days=item)
        if 1 == int(statdate_item.day):  # 月初统计上月月报
            enddate = statdate_item - datetime.timedelta(days=1)
            startdate = datetime.datetime.strptime(
                '%s-%s-%s' % (enddate.year, enddate.month, 1), '%Y-%m-%d')
            for stattype in STATTYPES:
                prepare_statdata(browser, stattype, startdate.strftime(
                    '%Y-%m-%d'), enddate.strftime('%Y-%m-%d'), 'month', 'room')
        # 更新统计日期
        set_option("arrange_room_statdate", statdate_item.strftime('%Y-%m-%d'))
    # 统计arrange_price_statdate
    statdate = datetime.datetime.strptime(
        get_option("arrange_price_statdate"), '%Y-%m-%d')
    delta = current_datetime - statdate
    for item in range(1, delta.days - STATDELTA):
        statdate_item = statdate + datetime.timedelta(days=item)
        if 1 == int(statdate_item.day):  # 月初统计上月月报
            enddate = statdate_item - datetime.timedelta(days=1)
            startdate = datetime.datetime.strptime(
                '%s-%s-%s' % (enddate.year, enddate.month, 1), '%Y-%m-%d')
            # 仅 成交情况 时统计价格区间
            prepare_statdata(browser, STATTYPES[0], startdate.strftime(
                '%Y-%m-%d'), enddate.strftime('%Y-%m-%d'), 'month', 'price')
        # 更新统计日期
        set_option("arrange_price_statdate",
                   statdate_item.strftime('%Y-%m-%d'))
    # 统计arrange_amount_statdate
    statdate = datetime.datetime.strptime(
        get_option("arrange_amount_statdate"), '%Y-%m-%d')
    delta = current_datetime - statdate
    for item in range(1, delta.days - STATDELTA):
        statdate_item = statdate + datetime.timedelta(days=item)
        if 1 == int(statdate_item.day):  # 月初统计上月月报
            enddate = statdate_item - datetime.timedelta(days=1)
            startdate = datetime.datetime.strptime(
                '%s-%s-%s' % (enddate.year, enddate.month, 1), '%Y-%m-%d')
            # 仅 成交情况 时统计价格区间
            prepare_statdata(browser, STATTYPES[0], startdate.strftime(
                '%Y-%m-%d'), enddate.strftime('%Y-%m-%d'), 'month', 'amount')
        # 更新统计日期
        set_option("arrange_amount_statdate",
                   statdate_item.strftime('%Y-%m-%d'))
    # 关闭浏览器
    close_browser(browser)
    # 更新区域
    cities = json.loads(get_option("cities"))
    current_cities = []
    for cts in cities:
        current_scopes = cts['children']
        scopes = [item['value'] for item in current_scopes]
        addition_scopes = []
        sqli = 'SELECT DISTINCT `scope` FROM `dataset_resume` WHERE `city`="%s"' % cts[
            'value']
        result = sql_query(sqli)
        for item in result:
            if item[0] not in scopes:
                addition_scopes.append({"value": item[0], "label": item[0], "center": {
                                       "lng": 0, "lng": 0}, "zoom": 0})
        current_scopes.extend(addition_scopes)
        sorted_scopes = sorted(
            current_scopes, key=lambda current_scopes: current_scopes['value'])
        cts['children'] = sorted_scopes
        current_cities.append(cts)
    set_option('cities', json.dumps(current_cities, ensure_ascii=False))
    # 更新户型和物业
    spiderman_frame = json.loads(get_option("spiderman_frame"))
    sqli = 'SELECT DISTINCT `property` FROM `dataset_resume`'
    result = sql_query(sqli)
    properties = [item[0] for item in result]
    spiderman_frame['property'].extend(
        list(set(properties).difference(set(spiderman_frame['property']))))
    sqli = 'SELECT DISTINCT `intervals` FROM `dataset_room`'
    result = sql_query(sqli)
    arrange_room = [item[0] for item in result]
    spiderman_frame['arrange']['room'].extend(
        list(set(arrange_room).difference(set(spiderman_frame['arrange']['room']))))
    set_option('spiderman_frame', json.dumps(
        spiderman_frame, ensure_ascii=False))
    # 更新项目位置
    sqli = 'SELECT `pro_name` FROM `projects` WHERE `pro_address` IS NULL'
    result = sql_query(sqli)
    for item in result:
        time.sleep(3)
        re = requests.get('http://api.map.baidu.com/place/v2/search?query=' +
                          item[0] + '&tag=%E6%88%BF%E5%9C%B0%E4%BA%A7&region=%E8%A5%BF%E5%AE%89%E5%B8%82&city_limit=true&output=json&ak=sUh3OWHYfFpcZoQqa0qN5g7x')
        jsondata = re.json()
        if jsondata['results']:
            for data in jsondata['results']:
                if difflib.SequenceMatcher(None, item[0], data['name']).quick_ratio() > 0.7:
                    sqli = 'UPDATE `projects` SET `pro_address`="%s",`pro_lng`="%s",`pro_lat`="%s" WHERE `pro_name`="%s"' % (
                        data['address'], data['location']['lng'], data['location']['lat'], item[0])
                    sql_exec(sqli)
                    break
