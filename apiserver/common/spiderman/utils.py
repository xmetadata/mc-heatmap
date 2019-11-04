# -*- coding: UTF-8 -*-
import pymysql

from config import DBSERVER


def sql_query(sqli, fetchone=False):
    # 打开数据库连接
    db = pymysql.connect(DBSERVER['host'],
                         DBSERVER['username'],
                         DBSERVER['password'],
                         DBSERVER['database'],
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


def sql_exec(sqli, executemany=None):
    # 打开数据库连接
    db = pymysql.connect(DBSERVER['host'],
                         DBSERVER['username'],
                         DBSERVER['password'],
                         DBSERVER['database'],
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
        print(e)
        # 发生错误时回滚
        db.rollback()
    finally:
        # 关闭数据库连接
        db.close()


def get_option(opt_key):
    # 获取选项值
    result = sql_query(
        'SELECT * FROM `options` WHERE `opt_key`="%s"' % opt_key, fetchone=True)
    return result[2]


def set_option(opt_key, opt_value):
    # 更新选项值
    sql_exec('UPDATE `options` SET `opt_value`=\'%s\' WHERE `opt_key`=\'%s\'' %
             (opt_value, opt_key))
