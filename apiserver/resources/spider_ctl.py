# -*- coding: UTF-8 -*-
import json
from celery.result import AsyncResult
from flask_restful import Resource, request
from flask_jwt import current_identity, jwt_required
#from common.data_spider.tasks.tasks_manager import tasks_manager
#from common.data_spider.tasks.proj_none import proj_none
#from common.data_spider.tasks.proj_subtask import proj_subtask
#from common.data_spider.spider_common.utils import db_query, db_exec
#from common.utils import StandardResponse

class SpiderCtl(Resource):
    def __init__(self):
        self.result__ = {
            "spider_status" : 0,
            "spider_none_status" : False,
            "spider_subtask_status" : False
        }

    def GetTaskInfo__(self):
        try:
            sql = "select opt_value from t_options_data where opt_key = 'spider_task_info'"
            result = db_query(sql)
            if not result:
                return False, StandardResponse(500, 1, u'SQLAlchemy Error')
            spider_info = json.loads(result[0][0])
            main_task_id = spider_info['main']['id']
            none_task_id = spider_info['none']['id']
            subtask_id = spider_info['subtask']['id']
            main_task = False#if len(main_task_id) == 0 else AsyncResult(id=main_task_id,
                                                                         #app=tasks_manager).successful()
            none_task = False# if len(none_task_id) == 0 else AsyncResult(id=none_task_id, app=proj_none).successful()
            sub_task = False# if len(subtask_id) == 0 else AsyncResult(id=subtask_id, app=proj_subtask).successful()
            status = 0
            if not main_task and not none_task and not sub_task:
                return False, StandardResponse(200, 0, data=self.result__)
            if main_task:
                self.result__['spider_status'] = 1
            else:
                return False, StandardResponse(200, 0, data=self.result__)
            if none_task:
                self.result__['spider_none_status'] = True
            if sub_task:
                self.result__['spider_subtask_status'] = True
            if self.result__['spider_status'] == 1:
                return True, StandardResponse(200, 0, data=self.result__)
            else:
                return False, StandardResponse(200, 0, data=self.result__)
        except Exception, e:
            return False, StandardResponse(500, 1, e.message)

    @jwt_required()
    def get(self):
        status, result = self.GetTaskInfo__()
        return result

    @jwt_required()
    def put(self):
        status, result = self.GetTaskInfo__()
        if status:
            return result
        try:
            sql = "select opt_value from options where opt_key = 'spider_task_info'"
            result = db_query(sql)
            if not result:
                return False, StandardResponse(500, 1, u'SQLAlchemy Error')
            spider_info = json.loads(result[0][0])
            spider_info['main']['id'] = ''
            spider_info['none']['id'] = ''
            spider_info['subtask']['id'] = ''
            update_sql = "update t_options_data set opt_value = '%s' " \
                         "where opt_key = 'spider_task_info'", json.dumps(spider_info)
            db_exec(update_sql)
            self.result__['spider_status'] = 1
            return StandardResponse(200, 0, data = self.result__)
        except Exception, e:
            return StandardResponse(500, 1, e.message)
