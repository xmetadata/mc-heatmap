# -*- coding: UTF-8 -*-
import json
import requests
from config.config import CURRENT_PROJECT, HEADERS, POOLSIZE, PROJECT_PAYLOAD, STATGAP, TEST_PAYLOAD, logger
from common.utils import db_exec, db_query, is_float, last_day_of_month
from tasks.proj_sync import proj_sync
from tasks.proj_subtask import proj_subtask
from config.config import app

#@app.task
def tasks_manager():
     logger.info("enter to task preprocess!")
     # 1.获取Cookie记录
     results = db_query(
         'select * from t_options_data where opt_key = "spider_cookie"', fetchone=True)
     HEADERS['Cookie'] = results[2]
    
     # 2.判断Cookie是否有效
     url = 'https://creis.fang.com/city/PropertyStatistics/DetailsAjax'
     try:
         r = requests.post(
             url, data={'jsonParameters': json.dumps(TEST_PAYLOAD)}, headers=HEADERS)
         json.loads(r.text)
     except Exception, e:
         logger.error(r.text)
         exit()
     logger.debug("end of task initialization!")
     proj_sync()
