# -*- coding: UTF-8 -*-
import logging

logging.basicConfig(level=logging.INFO,
                    filename='spiderman.log',
                    filemode='a',
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    )
logger = logging.getLogger('spiderman')

STATDELTA = 10

DBSERVER = {
    'host': '47.103.36.82',
    'username': 'root',
    'password': 'Aa888888',
    'database': 'heatmap',
}

STATTYPES = ['成交情况', '上市情况', '可售情况']

ACCOUNT_INFO = {
    'account' : 'sy-19110820',
    'passwd' : '123456',
    'token' : '0424',
}
