# -*- coding: UTF-8 -*-
from common.data_spider.tasks.tasks_manager import tasks_manager
from common.data_spider.tasks.proj_sync import proj_sync
from common.data_spider.tasks.proj_none import proj_none
from common.data_spider.tasks.proj_subtask import proj_subtask

class SpiderCtl():
    def __init__(self):
        self.result__ = {
            "spider_status" : False,
            "spider_none_status": "2019-09-15",
            "spider_date_arrange": "2019-09-01"
        }
    def get(self):
        pass
    def post(self):
        pass