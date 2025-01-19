import logging
import requests
import sqlite3
import time

from datetime import datetime, timezone, timedelta
from read_configuration import read_configuration

logger = logging.getLogger('my_logger')


# 读取 config.yaml 配置文件
def get_configuration():
    cookie, user_agent, referer, max_page, page_per_num = read_configuration('cookie', 'User-Agent', 'Referer',
                                                                             'MAX_PAGE', 'PAGE_PER_NUM')
    cookies = {i.split("=")[0]: i.split("=")[-1] for i in cookie.split("; ")}
    headers = {
        'User-Agent': user_agent,
        'Referer': referer,
    }
    max_page = max_page
    page_per_num = page_per_num
    return cookies, headers, max_page, page_per_num


def get_all_bili_history():
    cookies, headers, max_page, page_per_num = get_configuration()
    conn = sqlite3.connect('database/bilibili.db')
    cursor = conn.cursor()
    for page_num in range(max_page):
        time.sleep(0.6)
        url = 'https://api.bilibili.com/x/v2/history?pn={pn}&ps={ps}&jsonp=jsonp'.format(pn=page_num, ps=page_per_num)
        response = requests.get(url, headers=headers, cookies=cookies)
        data = response.json()['data']
        if data:
            logger.info(f"历史记录第{page_num}页: {len(data)}条记录")
            for h in data:
                mid = h['owner']['mid']
                name = h['owner']['name']
                view_time = h['view_at']
                utc_time = datetime.fromtimestamp(view_time, tz=timezone.utc)
                eastern_time = utc_time.astimezone(timezone(timedelta(hours=8)))
                cursor.execute('SELECT 1 FROM users WHERE mid = ? AND latest_time < ?', (mid, view_time))
                result = cursor.fetchone()
                if result:
                    cursor.execute('UPDATE users SET latest_time = ? WHERE mid = ?', (view_time, mid))
                    logger.info(f"更新up主--{name}最新观看时间为{eastern_time}")
        else:
            logger.info(f"历史记录第{page_num}页: 无数据")
    conn.commit()
    conn.close()
