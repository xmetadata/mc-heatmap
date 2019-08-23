import importlib
import requests
import json
import gevent
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
        cookie = db_query("select opt_value from options where opt_key='cookie'", fetchone=True)
        if not cookie:
            logger.error("ProjectSync::GenerateHeader [ " + self.project_name__ + \
                         "]: Export valid cookie.")
            return None
        self.config__['url_header']['Cookie'] = cookie
        return self.config__

    def __GeneratePayload(self, page):
        statistic_type = self.config__['statistic_type'][0]
        self.config__['url_payload']['sTypeName'] = statistic_type
        payload = self.config__['url_payload']
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
        while page_index <= project_count/count_of_one_page:
            payload = self.__GeneratePayload(page_index)
            try:
                response = requests.post( self.config__['statistic_url'], data={'jsonParameters': json.dumps(payload)}, headers=header)
            except Exception, e:
                logger.error("ProjectSync::ParseProjectLoop [ " + self.project_name__ + \
                         "]: request url unsuccessfully, errmsg: " + e.message)
                return
            project = cls()
            project_num = project.ParseRespon(response)
            if project_count == 1:
                if not project_count:
                    logger.error("ProjectSync::ParseProjectLoop [ " + self.project_name__ + \
                             "]: Parse response unsuccessfully.")
                    return
                project_count = project_num
            ++page_index
            project.DealResult()

class TaskMgr:
    def __init__(self):
        self.task_list__ = {}
        self.task_count__ = 0
        self.pool = gevent.Pool(POOLSIZE)
        self.__TaskLoad()

    def __TaskLoad(self):
        for key, value in TASK_REGISTER:
            self.task_list__[key] = Task(value)
            self.task_count__ += 1

    def __TasksRun(self):
        for key, value in self.task_list__:
            logger.info("TaskMgr::__TasksRun: start run level [" + key + "] task......")
            jobs = [gevent.spawn(task.ParseProjectLoop()) for task in value]
            gevent.joinall(jobs)
            logger.info("TaskMgr::__TaskRun: end run level [" + key + "] task......")
        logger.info("TaskMgr::__TaskRun: all tasks are processed.")

    def Run(self):
        self.__TasksRun()