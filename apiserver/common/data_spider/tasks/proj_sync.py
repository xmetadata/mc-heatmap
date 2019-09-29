# -*- coding: UTF-8 -*-
import requests
import json
#import timeit
from datetime import datetime, timedelta
from uuid import uuid1
from urllib2 import unquote, quote
from celeryapp import app
from config.config import logger, HEADERS, PROJECT_PAYLOAD, TEST_PAYLOAD, STATGAP, CURRENT_PROJECT
from common.utils import db_exec, db_query, is_float
from config.config import app
from proj_none import proj_none
#from proj_subtask import proj_subtask

@app.task
def proj_sync():
    logger.info('Synchronize project start...')
    # 获取已入库项目列表
    sql = 'select * from projects'
    results = db_query(sql)
    has_project = [row[1] for row in results]
    # 发现新项目
    temp_project = []
    disc_project = []
    url = 'https://creis.fang.com/city/Property/GetPropertySearchInterface/'
    for key, value in PROJECT_PAYLOAD.items():
        # 确定有多少项目需要同步
        data = {
            'jsonParameters': json.dumps({
                "urlParams": quote(json.dumps(value)),
                "proids": "",
                "type": key,
            })
        }
        r = requests.post(url, data=data, headers=HEADERS)
        r_json = json.loads(r.text)
        totalCount = int(r_json['totalCount'])
        # 从第一页开始同步全部
        for i in range(1, int(int(totalCount)/100) + 2):
            value['iPageIndex'] = str(i)
            data = {
                'jsonParameters': json.dumps({
                    "urlParams": quote(json.dumps(value)),
                    "proids": "",
                    "type": key,
                })
            }
            r = requests.post(url, data=data, headers=HEADERS)
            r_json = json.loads(r.text)
            for project in r_json['Table']:
                if project['title'] not in has_project:
                    if project['title'] not in temp_project:
                        temp_project.append(project['title'])
                        if is_float(project['y']) and is_float(project['y']):
                            disc_project.append((uuid1().hex, project['title'], unquote(project['address'].encode(
                                'UTF-8', 'ignore')).decode('UTF-8', 'ignore'), round(float(project['x']), 6), round(float(project['y']), 6)))
    # 入库新项目
    sql = 'insert into projects(pro_uuid, pro_name, pro_address, pro_lat, pro_lng) values(%s, %s, %s, %s, %s)'
    db_exec(sql, executemany=disc_project)
    # 最新项目列表
    logger.info('Refresh global CURRENT_PROJECT.')
    sql = 'select * from projects'
    results = db_query(sql)
    global CURRENT_PROJECT
    for row in results:
        CURRENT_PROJECT[row[1]] = row[0]
    logger.info('Synchronize project finish.')
    proj_none.delay()
    #proj_subtask.delay()
