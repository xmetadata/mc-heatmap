# -*- coding: UTF-8 -*-
import datetime
from uuid import uuid1

import MySQLdb

from task_config import DB

import logging

logging.basicConfig(level=logging.INFO,
                    filename='synctask.log',
                    filemode='a',
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    )
logger = logging.getLogger('synctask')

def get_uuid():
    return uuid1().hex

def db_query(sqli, fetchone=False):
    # 打开数据库连接
    db = MySQLdb.connect(DB['host'],
                         DB['username'],
                         DB['password'],
                         DB['database'],
                         charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # 使用execute方法执行SQL语句
    cursor.execute(sqli)

    if not fetchone:
        # 获取所有记录列表
        data = cursor.fetchall()
    else:
        # 使用 fetchone() 方法获取一条数据
        data = cursor.fetchone()

    # 关闭数据库连接
    db.close()

    # 返回查询结果
    return data


def db_exec(sqli, executemany=None):
    # 打开数据库连接
    db = MySQLdb.connect(DB['host'],
                         DB['username'],
                         DB['password'],
                         DB['database'],
                         charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 更新语句
    try:
        if executemany is None:
            # 执行SQL语句
            cursor.execute(sqli)
        else:
            # 执行批量插入SQL语句
            cursor.executemany(sqli, executemany)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        logger.error(e.message)
        logger.error(sqli)
        logger.error(executemany)
        # 发生错误时回滚
        db.rollback()
    finally:
        # 关闭数据库连接
        db.close()


def is_float(x):
    """ 判断浮点数 """
    try:
        float(x)
        return True
    except:
        return False


def last_day_of_month(any_day):
    """
    获取获得一个月中的最后一天
    :param any_day: 任意日期
    :return: string
    """
    next_month = any_day.replace(
        day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)
