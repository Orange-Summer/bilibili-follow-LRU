import datetime
import logging
import requests
import sqlite3

from read_configuration import read_configuration

logger = logging.getLogger('my_logger')


# 读取 config.yaml 配置文件
def get_configuration():
    cookie, user_agent, referer = read_configuration('cookie', 'User-Agent', 'Referer')
    cookies = {i.split("=")[0]: i.split("=")[-1] for i in cookie.split("; ")}
    headers = {
        'User-Agent': user_agent,
        'Referer': referer,
    }
    return cookies, headers


# 获取你关注的UP主列表
def get_following_up_list(page, user_id):
    cookies, headers = get_configuration()
    url = f'https://api.bilibili.com/x/relation/followings?vmid={user_id}&pn={page}&ps=50&order=desc&jsonp=jsonp'
    response = requests.get(url, headers=headers, cookies=cookies)
    return response.json()


# 获取所有关注的UP主名字和链接
def get_all_following_up_details(user_id):
    page = 1
    conn = sqlite3.connect('database/bilibili.db')
    cursor = conn.cursor()
    add_num = 0
    cursor.execute("SELECT COUNT(*) FROM users")
    total_count = cursor.fetchone()[0]
    total_count_new = 0
    mid_list = []
    curr_time = int(datetime.datetime.now().timestamp())
    while True:
        data = get_following_up_list(page, user_id)
        if 'data' not in data:
            print(f"Error fetching data for page {page}: {data}")
            break
        followings = data['data']['list']
        if not followings:
            break
        mid_list = mid_list + [up['mid'] for up in followings]
        for up in followings:
            up_name = up['uname']
            up_mid = up['mid']
            cursor.execute('SELECT 1 FROM users WHERE mid = ?', (up_mid,))
            result = cursor.fetchone()
            if result:
                total_count_new += 1
            else:
                cursor.execute('INSERT INTO users (mid, name,latest_time) VALUES (?, ?, ?)',
                               (up_mid, up_name, curr_time))
                total_count_new += 1
                add_num += 1

        page += 1
    placeholders = ', '.join(['?'] * len(mid_list))
    sql = f"DELETE FROM users WHERE mid NOT IN ({placeholders})"
    cursor.execute(sql, mid_list)
    logger.info(
        f"数据库存在{total_count}名up主，新增{add_num}名up主，取关{total_count + add_num - total_count_new}名up主，现在关注{total_count_new}名up主")
    conn.commit()
    conn.close()
