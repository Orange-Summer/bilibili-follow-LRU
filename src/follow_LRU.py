import logging
import sqlite3
import time

logger = logging.getLogger('my_logger')


def iterate_users():
    conn = sqlite3.connect('database/bilibili.db')
    cursor = conn.cursor()
    curr_time = int(time.time())
    one_month_ago_time = curr_time - 30 * 24 * 60 * 60
    three_month_ago_time = curr_time - 30 * 24 * 60 * 60 * 3
    cursor.execute('SELECT name, mid FROM users WHERE latest_time > 0 AND latest_time < ?', (one_month_ago_time,))
    one_month_ago = cursor.fetchall()
    logger.info(f"一个月未观看的up有{len(one_month_ago)}名")
    cursor.execute('SELECT name, mid FROM users WHERE latest_time > 0 AND latest_time < ?', (three_month_ago_time,))
    three_month_ago = cursor.fetchall()
    logger.info(f"三个月未观看的up有{len(one_month_ago)}名")
    conn.close()
    return one_month_ago, three_month_ago
