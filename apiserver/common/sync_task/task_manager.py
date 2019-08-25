import importlib
import requests
import json
import gevent.pool as g_pool
from project_utils import logger, db_query
from task_config import PROJECT_SYNC, MODULES, TASK_REGISTER, POOLSIZE

class Task:
    def __init__(self, project_name):
        self.config__ = PROJECT_SYNC
        self.project_name__ = project_name

    def __GenerateProjectClass(self):
        for itr in MODULES:
            module = importlib.import_module(itr)
            cls = getattr(module, self.project_name__)
            if cls:
                return cls
        return None

    def __GenerateHeader(self):
        cookie = db_query("select opt_value from t_options_data where opt_key='cookie'", fetchone=True)
        if not cookie:
            logger.error("ProjectSync::GenerateHeader [ " + self.project_name__ + \
                         "]: Export valid cookie.")
            return None
        self.config__['url_header']['Cookie'] = cookie[0]
        return self.config__['url_header']

    def __GeneratePayload(self, page):
        statistic_type = self.config__['statistic_type'][0]
        payload = self.config__['url_payload']
        payload['sTypeName'] = statistic_type
        payload['iPageIndex'] = page
        return payload

    def ParseProjectLoop(self):
        cls = self.__GenerateProjectClass()
        if not cls:
            logger.error("ProjectSync::ParseProjectLoop [ " + self.project_name__ + \
                         "]: generate " + self.project_name__ + " class unsuccessfully.")
            return
        project_count = 1
        count_of_one_page = self.config__['url_payload']['iPageSize']
        header = self.__GenerateHeader()
        page_index = 1
        page_statistic = 0
        while project_count == 1 or page_index <= int(project_count/int(count_of_one_page)) + page_statistic:
            payload = self.__GeneratePayload(page_index)
            try:
                response = requests.post( self.config__['statistic_url'],
                             data={'jsonParameters': json.dumps(payload)}, headers=header)
            except Exception, e:
                logger.error("ProjectSync::ParseProjectLoop [ " + self.project_name__ + \
                         "]: request url unsuccessfully, errmsg: " + e.message)
                return
            project = cls()
            project_num = project.ParseRespon(response.text)
            if project_count == 1:
                if not project_count:
                    logger.error("ProjectSync::ParseProjectLoop [ " + self.project_name__ + \
                             "]: Parse response unsuccessfully.")
                    return
                page_statistic = 1 if project_count%int(count_of_one_page) else 0
                project_count = project_num
            page_index += 1
            project.ProcessResult()

class TaskMgr:
    def __init__(self):
        self.task_list__ = {1: [], 2: [], 3: [], 4: [], 5: []}
        self.task_count__ = 0
        self.pool = g_pool.Pool(POOLSIZE)
        self.__TaskLoad()

    def __TaskLoad(self):
        for key, value in TASK_REGISTER.items():
            for itr in value:
                self.task_list__[key].append(Task(itr))
                self.task_count__ += 1

    def __TasksRun(self):
        for key, value in self.task_list__.items():
            logger.info("TaskMgr::__TasksRun: start run level [%d] task......" %(key))
            jobs = [self.pool.spawn(task.ParseProjectLoop()) for task in value]
            for itr in jobs:
                itr.join()
            logger.info("TaskMgr::__TaskRun: end run level [%d] task......" %(key))
        logger.info("TaskMgr::__TaskRun: all tasks are processed.")

    def Run(self):
        self.__TasksRun()