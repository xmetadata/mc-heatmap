# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta
import json
from uuid import uuid1
import requests
from config.config import logger, HEADERS, PROJECT_PAYLOAD, TEST_PAYLOAD, STATGAP, POOLSIZE, CURRENT_PROJECT
from common.utils import db_exec, db_query, is_float, last_day_of_month
from gevent import monkey
from gevent.pool import Pool
from config.config import app

def download_dataset(param):
    collector = []
    payload = {
        "sTypeName": "",
        "sCityID": "",
        "sDealDataTableType": "week",
        "dBeginDate": "",
        "dEndDate": "",
        "sPropertyDistrictIds": "",
        "sPropertyTypeIds": "",
        "sBoardIds": "",
        "sRoomTypeIds": "",
        "sCityZoneIds": "",
        "fRoomAreaBegin": "",
        "fRoomAreaEnd": "",
        "fRoomPriceBegin": "",
        "fRoomPriceEnd": "",
        "fRoomAmountBegin": "",
        "fRoomAmountEnd": "",
        "iTotalFloorBegin": "",
        "iTotalFloorEnd": "",
        "sPropertyName": "",
        "sOrderName": "dealnum",
        "sOrderType": "desc",
        "iPageIndex": "1",
        "iPageSize": "100",
    }
    payload['sTypeName'] = param['stattype']
    # 可售情况仅月末统计
    if param['stattype'] == u'可售情况':
        payload['dBeginDate'] = param['statdate'].strftime("%Y-%m")
        payload['dEndDate'] = 'undefined'
    else:
        payload['dBeginDate'] = param['statdate'].strftime("%Y-%m-%d")
        payload['dEndDate'] = param['statdate'].strftime("%Y-%m-%d")
    payload['sCityID'] = param['city'].split(':')[1]
    payload['sPropertyTypeIds'] = param['property'].split(':')[1]
    if param['arrange']['type'] == 'room':  # 房型
        payload['sRoomTypeIds'] = param['arrange']['room'].split(':')[1]
        arrange = param['arrange']['room'].split(':')[0]
        table = 'dataset_room'
    elif param['arrange']['type'] == 'area':  # 面积
        payload['fRoomAreaBegin'] = param['arrange']['from']
        payload['fRoomAreaEnd'] = param['arrange']['to']
        arrange = param['arrange']['from']
        table = 'dataset_area'
    elif param['arrange']['type'] == 'amount':  # 总价
        payload['fRoomAmountBegin'] = param['arrange']['from']
        payload['fRoomAmountEnd'] = param['arrange']['to']
        arrange = param['arrange']['from']
        table = 'dataset_amount'
    elif param['arrange']['type'] == 'price':  # 单价
        payload['fRoomPriceBegin'] = param['arrange']['from']
        payload['fRoomPriceEnd'] = param['arrange']['to']
        arrange = param['arrange']['from']
        table = 'dataset_price'
    else:
        arrange = ''
        table = 'dataset_none'
    url = 'https://creis.fang.com/city/PropertyStatistics/DetailsAjax'
    try:
        r = requests.post(
        url, data={'jsonParameters': json.dumps(payload)}, headers=HEADERS)
        r_json = json.loads(r.text)
    except Exception, e:
        logger.warn("request url unsuccessfully.")
    if r_json.has_key('result'):
        return
    collector.extend(r_json['Table1'])
    pages = int(int(r_json['Table'][0]['Column1'])/100)
    if pages > 0:
        for pg in range(2, pages + 2):
            payload['iPageIndex'] = pg
            r = requests.post(
                url, data={'jsonParameters': json.dumps(payload)}, headers=HEADERS)
            r_json = json.loads(r.text)
            if r_json.has_key('result'):
                continue
            collector.extend(r_json['Table1'])
    if collector:
        sql = 'DELETE FROM dataset_none WHERE stattype="%s" AND statdate="%s" AND city="%s" AND property="%s" AND arrange="%s"' % (
            param['stattype'], param['statdate'].strftime("%Y-%m-%d"), param['city'].split(':')[0], param['property'].split(':')[0], arrange)
        db_exec(sql)
        data = []
        for item in collector:
            if CURRENT_PROJECT.has_key(item['sPropertyName']):
                if item['fRoomArea'] < 0:
                    item['fRoomArea'] = 0
                if param['stattype'] == u'成交情况':
                    data.append([uuid1().hex, param['stattype'], param['statdate'].strftime("%Y-%m-%d"), CURRENT_PROJECT[item['sPropertyName']], param['city'].split(
                        ':')[0], item['sDistrictName'], param['property'].split(':')[0], arrange, item['iDealNum'], item['fRoomArea'], item['fRoomAmount']])
                elif param['stattype'] == u'上市情况':
                    data.append([uuid1().hex, param['stattype'], param['statdate'].strftime("%Y-%m-%d"), CURRENT_PROJECT[item['sPropertyName']], param['city'].split(
                        ':')[0], item['sDistrictName'], param['property'].split(':')[0], arrange, item['iNum'], item['fRoomArea'], 0])
                else:
                    data.append([uuid1().hex, param['stattype'], param['statdate'].strftime("%Y-%m-%d"), CURRENT_PROJECT[item['sPropertyName']], param['city'].split(
                        ':')[0], item['sDistrictName'], param['property'].split(':')[0], arrange, item['iNum'], item['fRoomArea'], 0])
        sql = 'INSERT INTO ' + table + \
            '(uuid, stattype, statdate, pro_uuid, city, scope, property, arrange, number, area, amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        db_exec(sql, data)

def sub_sync(spider_args, statdate):
    logger.info('Synchronize dataset start...')
    logger.info('StatDate: ' + statdate.strftime("%Y-%m-%d"))
    pool = Pool(POOLSIZE)
    for city in spider_args['city']:
        logger.info('City: ' + city)
        for stattype in spider_args['stattype']:
            logger.info('StatType: ' + stattype)
            # 仅在月末统计可售情况
            if stattype == u'可售情况' and statdate != last_day_of_month(statdate):
                continue
            for property in spider_args['property']:
                logger.info('Property: ' + property)
                # 按房型排序
                logger.info('Arrange: room')
                for item in spider_args['arrange']['room']:
                    param = {
                        "statdate": statdate,
                        "city": city,
                        "stattype": stattype,
                        "property": property,
                        "arrange": {
                            "type": "room",
                            "room": item
                        }
                    }
                    pool.spawn(download_dataset, param)

                # 按面积排序
                logger.info('Arrange: area')
                for item in range(spider_args['arrange']['area'][0], spider_args['arrange']['area'][1], spider_args['arrange']['area'][2]):
                    param = {
                        "statdate": statdate,
                        "city": city,
                        "stattype": stattype,
                        "property": property,
                        "arrange": {
                            "type": "area",
                            "from": item,
                            "to": item + spider_args['arrange']['area'][2] - 1
                        }
                    }
                    pool.spawn(download_dataset, param)
                param = {
                    "statdate": statdate,
                    "city": city,
                    "stattype": stattype,
                    "property": property,
                    "arrange": {
                        "type": "area",
                        "from": spider_args['arrange']['area'][1],
                        "to": ""
                    }
                }
                pool.spawn(download_dataset, param)

                # 成交情况 需要按照单价和总价统计
                if stattype == u'成交情况':
                    # 按价格排序
                    logger.info('Arrange: price')
                    for item in range(spider_args['arrange']['price'][0], spider_args['arrange']['price'][1], spider_args['arrange']['price'][2]):
                        param = {
                            "statdate": statdate,
                            "city": city,
                            "stattype": stattype,
                            "property": property,
                            "arrange": {
                                "type": "price",
                                "from": item,
                                "to": item + spider_args['arrange']['price'][2] - 1
                            }
                        }
                        pool.spawn(download_dataset, param)
                    param = {
                        "statdate": statdate,
                        "city": city,
                        "stattype": stattype,
                        "property": property,
                        "arrange": {
                            "type": "price",
                            "from": spider_args['arrange']['price'][1],
                            "to": ""
                        }
                    }
                    pool.spawn(download_dataset, param)

                    # 按总价排序
                    logger.info('Arrange: amount')
                    for item in range(spider_args['arrange']['amount'][0], spider_args['arrange']['amount'][1], spider_args['arrange']['amount'][2]):
                        param = {
                            "statdate": statdate,
                            "city": city,
                            "stattype": stattype,
                            "property": property,
                            "arrange": {
                                "type": "amount",
                                "from": item,
                                "to": item + spider_args['arrange']['amount'][2] - 1
                            }
                        }
                        pool.spawn(download_dataset, param)
                    param = {
                        "statdate": statdate,
                        "city": city,
                        "stattype": stattype,
                        "property": property,
                        "arrange": {
                            "type": "amount",
                            "from": spider_args['arrange']['amount'][1],
                            "to": ""
                        }
                    }
                    pool.spawn(download_dataset, param)
    pool.join()
    logger.info('Synchronize dataset finish.  ' +
                statdate.strftime("%Y-%m-%d"))

@app.task
def proj_subtask():
    sql = 'update t_options_data set opt_value = 1 where opt_key = "spider_status"'
    db_exec(sql)
    # 获取爬虫参数
    results = db_query(
        'select * from t_options_data where opt_key = "spider_args"', fetchone=True)
    spider_args = json.loads(results[2])
    logger.info('Spider args: ' + json.dumps(spider_args, indent=2))

    # 按日期爬取
    results = db_query(
        'select * from t_options_data where opt_key = "spider_at"', fetchone=True)
    spider_at = datetime.strptime(results[2], "%Y-%m-%d")
    days = (datetime.now() + timedelta(days=STATGAP) - spider_at).days
    for num in range(1, days - 14):
        statdate = spider_at + timedelta(days=num)
        sub_sync(spider_args, statdate)
        sql = 'update t_options_data set opt_value = "%s" where opt_key = "spider_at"' % statdate.strftime(
            "%Y-%m-%d")
        db_exec(sql)
    sql = 'update t_options_data set opt_value = 0 where opt_key = "spider_none_status"'
    db_exec(sql)
