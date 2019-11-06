# -*- coding: UTF-8 -*-
import logging
import re
import time
from uuid import uuid1
import random
import pdb

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import COOKIES
from utils import sql_exec, sql_query, get_option, set_option


def initialize_browser():
    chrome_options = webdriver.ChromeOptions()
    # 使用headless无界面浏览器模式
    # chrome_options.add_argument('--headless')  # 增加无界面选项
    # 启动浏览器
    browser = webdriver.Chrome(
        r'D:\Python37\Scripts\chromedriver.exe', chrome_options=chrome_options)
    browser.implicitly_wait(3)  # 隐性等待时间3秒
    browser.get('https://creis.fang.com/')
    for cookie in COOKIES:
        browser.add_cookie(cookie)
    browser.get('https://creis.fang.com/city/PropertyStatistics/Details')
    browser.maximize_window()
    return browser


def close_browser(browser):
    browser.quit()


def handle_locator(browser, locator):
    try:
        return browser.find_element_by_css_selector(locator)
    except NoSuchElementException as e:
        logging.exception(e)
        pdb.set_trace()
    except Exception as e:
        logging.exception(e)
        pdb.set_trace()


def handle_text(browser, locator):
    try:
        return browser.find_element_by_css_selector(locator).text
    except NoSuchElementException as e:
        logging.exception(e)
        pdb.set_trace()
    except Exception as e:
        logging.exception(e)
        pdb.set_trace()


def handle_attribute(browser, attribute,  locator):
    try:
        return browser.find_element_by_css_selector(locator).get_attribute(attribute)
    except NoSuchElementException as e:
        logging.exception(e)
        pdb.set_trace()
    except Exception as e:
        logging.exception(e)
        pdb.set_trace()


def handle_click(browser, locator):
    try:
        time.sleep(random.randint(1, 3))
        WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, locator)))
        browser.find_element_by_css_selector(locator).click()
    except NoSuchElementException as e:
        logging.exception(e)
        pdb.set_trace()
    except ElementClickInterceptedException as e:
        logging.exception(e)
        pdb.set_trace()
    except Exception as e:
        logging.exception(e)
        pdb.set_trace()


def handle_input(browser, locator, content):
    try:
        time.sleep(random.randint(1, 3))
        browser.find_element_by_css_selector(locator).clear()
        browser.find_element_by_css_selector(locator).send_keys(content)
    except NoSuchElementException as e:
        logging.exception(e)
        pdb.set_trace()
    except Exception as e:
        logging.exception(e)
        pdb.set_trace()


def prepare_statdata(browser, stattype, startdate, enddate, datetype, arrange=None):
    """
    上传数据
    :param
        stattype: 成交情况/上市情况/可售情况
        startdate: datetime
        enddate: datetime
        datetype: day/month
        arrange: amount/price/area/room
    :return: None
    """
    #清空输入框，初始化最新查询
    handle_click(browser, '#ulLeftMenu > li:nth-child(2) > dl > dd:nth-child(1) > a')
    logging.info("begin to sleep 30 seconds!")
    time.sleep(30)
    logging.info("end of sleepping 30 seconds!")
    # 统计类型
    stattype_locator_dict = {
        '成交情况': '#type > li:nth-child(1) > a',
        '上市情况': '#type > li:nth-child(2) > a',
        '可售情况': '#type > li:nth-child(3) > a',
    }
    handle_click(browser, stattype_locator_dict[stattype])
    # 统计日期
    if stattype == '可售情况':
        browser.execute_script(
            'document.getElementById("dBeginDate").removeAttribute("readonly")')
        handle_input(browser, '#dBeginDate', startdate[:7])
    else:
        browser.execute_script(
            'document.getElementById("dBeginDate").removeAttribute("readonly")')
        handle_input(browser, '#dBeginDate', startdate)
        browser.execute_script(
            'document.getElementById("dEndDate").removeAttribute("readonly")')
        handle_input(browser, '#dEndDate', enddate)
    # 属性统计
    if arrange == 'amount':
        def arrange_amount(browser, stattype, startdate, datetype, arrange, interval, next_interval):
            # 判断next_interval
            if interval == int(get_option("arrange_amount_next_interval")):
                handle_input(browser, '#finalPriceBegin',
                             1 if interval == 0 else interval)
                handle_input(browser, '#finalPriceEnd',
                             '' if next_interval == 0 else next_interval)
                statdata_by_properties(
                    browser, stattype, startdate, datetype, arrange, interval)
                # 更新next_interval
                set_option("arrange_amount_next_interval", next_interval)

        arrange_amount(browser, stattype, startdate, datetype, arrange, 0, 40)
        for interval in range(40, 300, 10):
            arrange_amount(browser, stattype, startdate,
                           datetype, arrange, interval, interval + 10)
        arrange_amount(browser, stattype, startdate, datetype, arrange, 300, 0)
    elif arrange == 'price':
        def arrange_price(browser, stattype, startdate, datetype, arrange, interval, next_interval):
            # 判断next_interval
            if interval == int(get_option("arrange_price_next_interval")):
                handle_input(browser, '#dealPriceBegin',
                             1 if interval == 0 else interval)
                handle_input(browser, '#dealPriceEnd',
                             '' if next_interval == 0 else next_interval)
                statdata_by_properties(
                    browser, stattype, startdate, datetype, arrange, interval)
                # 更新next_interval
                set_option("arrange_price_next_interval", next_interval)

        arrange_price(browser, stattype, startdate, datetype, arrange, 0, 6000)
        for interval in range(6000, 30000, 1000):
            arrange_price(browser, stattype, startdate, datetype,
                          arrange, interval, interval + 1000)
        arrange_price(browser, stattype, startdate,
                      datetype, arrange, 30000, 0)
    elif arrange == 'area':
        def arrange_area(browser, stattype, startdate, datetype, arrange, interval, next_interval):
            # 判断next_interval
            if interval == int(get_option("arrange_area_next_interval")):
                handle_input(browser, '#roomAreaBegin',
                             1 if interval == 0 else interval)
                handle_input(browser, '#roomAreaEnd',
                             '' if next_interval == 0 else next_interval)
                statdata_by_properties(
                    browser, stattype, startdate, datetype, arrange, interval)
                # 更新next_interval
                set_option("arrange_area_next_interval", next_interval)

        arrange_area(browser, stattype, startdate, datetype, arrange, 0, 60)
        for interval in range(60, 180, 10):
            arrange_area(browser, stattype, startdate,
                         datetype, arrange, interval, interval + 10)
        arrange_area(browser, stattype, startdate, datetype, arrange, 180, 0)
    elif arrange == 'room':
        # 暂时不支持断点续传
        for item in handle_locator(browser, '#HouseTypeMore > div:nth-child(2)').find_elements_by_tag_name('a'):
            interval = handle_attribute(item, 'innerText', 'span > span')
            handle_click(browser, '#HouseTypeOne > em')
            handle_click(
                browser, '#HouseTypeMore > div.butbox > span:nth-child(1)')
            handle_click(
                browser, '#HouseTypeMore > div.butbox > span:nth-child(2)')
            item.click()
            handle_click(
                browser, '#HouseTypeMore > div.butbox > a.but_confirm')
            statdata_by_properties(
                browser, stattype, startdate, datetype, arrange, interval)
    else:
        statdata_by_properties(
            browser, stattype, startdate, datetype, None, None)


def statdata_by_properties(browser, stattype, statdate, datetype, arrange, interval):
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
          stattype, statdate, datetype, arrange, interval)
    projects = get_projects()
    table_suffix = arrange if arrange else 'resume'
    # 清空重复数据
    if arrange:
        sqli = 'DELETE FROM `dataset_%s` WHERE `stattype`="%s" AND `statdate`="%s" AND `datetype`="%s" AND `intervals`="%s"' % (
            table_suffix, stattype, statdate, datetype, interval)
    else:
        sqli = 'DELETE FROM `dataset_%s` WHERE `stattype`="%s" AND `statdate`="%s" AND `datetype`="%s"' % (
            table_suffix, stattype, statdate, datetype)
    sql_exec(sqli)
    # 按物业类型统计
    for item in handle_locator(browser, '#TenementMore > div:nth-child(2)').find_elements_by_tag_name('a'):
        properties = handle_attribute(item, 'innerText', 'span > span')
        handle_click(browser, '#TenementOne')
        handle_click(
            browser, '#TenementMore > div.butbox > span:nth-child(1)')
        handle_click(
            browser, '#TenementMore > div.butbox > span:nth-child(2)')
        item.click()
        handle_click(browser, '#TenementMore > div.butbox > a.but_confirm')
        # 加载数据
        loaddata = loaddata_by_stattype(browser, stattype)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
              properties, len(loaddata) if loaddata else 0)
        if loaddata:
            data = []
            for item in loaddata:
                # 新增项目
                if item[0] not in projects:
                    sqli = 'INSERT INTO `projects`(`pro_uuid`, `pro_name`) VALUES ("%s", "%s")' % (
                        uuid1().hex, item[0])
                    sql_exec(sqli)
                    projects = get_projects()
                data.append([uuid1().hex, projects[item[0]], "西安市", item[1], statdate, datetype,
                             properties, interval, stattype, item[2], item[3], item[4] if stattype == '成交情况' else 0])
            sqli = 'INSERT INTO `dataset_' + table_suffix + \
                '`(`uuid`, `pro_uuid`, `city`, `scope`, `statdate`, `datetype`, `property`, `intervals`, `stattype`, `number`, `area`, `amount`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            sql_exec(sqli, executemany=data)


def loaddata_by_stattype(browser, stattype):
    handle_click(
        browser, '#searchConditionDiv > div > div:nth-child(14) > div.form-input.fg_w02.fl > a')
    loading(browser)  # 加载数据
    result_number = int(handle_text(browser, '#resultNum'))
    if not result_number:
        return
    # 大于50条数据，则设置100每页
    if result_number > 60:
        set_pagesize(browser)
    # 分页下载数据
    page_content_line = []
    while True:
        if stattype == '成交情况':
            page_content_line.extend(handle_text(
                browser, '#result > tbody').split('\n')[7:-2])
        else:
            page_content_line.extend(handle_text(
                browser, '#result > tbody').split('\n')[3:-2])
        # 翻页
        if u'›' in handle_text(browser, '#listPager'):
            pager_length = len(handle_locator(
                browser, '#listPager').find_elements_by_tag_name('li'))
            handle_click(
                browser, '#listPager > li:nth-child(%d) > a > font' % pager_length)
            loading(browser)  # 加载数据
        else:
            break
    page_content = '\n'.join(page_content_line)
    page_content = page_content.replace('-', '0')
    pattern = re.compile(r'^(\S+)\s+(\S+)\s+\S+\s+\S+\s+(\d+)\s+(\d+)\s+\S+\s+([0-9.]+)\s+\S+\s+\S+$', flags=re.M) if stattype == '成交情况' else re.compile(
        r'^(\S+)\s+(\S+)\s+\S+\s+\S+\s+(\d+)\s+(\d+)$', flags=re.M)
    return pattern.findall(page_content)


def set_pagesize(browser):
    handle_click(browser, '#spanSize')
    handle_click(browser, '#divPageSize > a:nth-child(4)')
    loading(browser)  # 加载数据


def loading(browser):
    # 处理加载数据
    try:
        locator = (By.CSS_SELECTOR, '#divContent > div.mOverlay')
        WebDriverWait(browser, 60).until_not(
            EC.presence_of_element_located(locator))
    except TimeoutException as e:
        logging.exception(e)
    finally:
        return


def get_projects():
    # 获取项目信息并生成字典
    sqli = 'SELECT * FROM `projects`'
    result = sql_query(sqli)
    projects = {}
    for item in result:
        projects[item[1]] = item[0]
    return projects
