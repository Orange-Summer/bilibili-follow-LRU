import logging
import requests
import sqlite3

from read_configuration import read_configuration

logger = logging.getLogger('my_logger')


# 读取 config.yaml 配置文件
def get_configuration():
    cookie, user_agent, referer = read_configuration('cookie', 'User-Agent', 'Referer')
    cookies = {i.split("=")[0]: i.split("=")[-1] for i in cookie.split("; ")}
    headers = {  # 我这里用的是chrome浏览器
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
    old = 0
    new = 0
    while True:
        data = get_following_up_list(page, user_id)
        if 'data' not in data:
            print(f"Error fetching data for page {page}: {data}")
            break
        followings = data['data']['list']
        if not followings:
            break
        for up in followings:
            up_name = up['uname']
            up_mid = up['mid']
            cursor.execute('SELECT 1 FROM users WHERE mid = ?', (up_mid,))
            result = cursor.fetchone()
            if result:
                old += 1
            else:
                cursor.execute('INSERT INTO users (mid, name,latest_time) VALUES (?, ?, ?)', (up_mid, up_name, -1))
                new += 1
        page += 1
    logger.info(f"检索{old + new}名关注up主，存在{old}名up主，新增{new}名up主")
    conn.commit()
    conn.close()
