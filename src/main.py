import datetime
import logging
import schedule
import sys
import time

from bilibili_history import get_all_bili_history
from follow_LRU import iterate_users
from followed_content_creator_crawler import get_all_following_up_details
from logging.handlers import RotatingFileHandler
from read_configuration import read_configuration
from send_telegram import send_message
from database import create_database


def send_message_to_telegram(one_month_ago, three_month_ago):
    if len(one_month_ago) > 0:
        one_month_result = "\n".join([f"{name} https://space.bilibili.com/{mid}" for name, mid in one_month_ago])
    else:
        one_month_result = "无"
    one_month_result = "一个月未观看的up主\n" + one_month_result
    if len(three_month_ago) > 0:
        three_month_result = "\n".join([f"{name} https://space.bilibili.com/{mid}" for name, mid in three_month_ago])
    else:
        three_month_result = "无"
    three_month_result = "三个月未观看的up主\n" + three_month_result
    result = str(datetime.date.today()) + "\n" + one_month_result + "\n" + three_month_result
    send_message(result)


def job():
    logger.info("------------Job Start------------")
    # 获取用户ID
    [user_id] = read_configuration('user_id')
    logger.info(f"User id: {user_id}")

    # 更新关注up主列表
    get_all_following_up_details(user_id)
    # 更新up主最新观看时间
    get_all_bili_history()
    # 查询一个月和三个月未观看的up主
    one_month_ago, three_month_ago = iterate_users()
    # telegram bot发送消息
    send_message_to_telegram(one_month_ago, three_month_ago)
    logger.info("------------Job End------------")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(filename)s [line:%(lineno)d] - %(levelname)s - %(message)s",
                                  '%Y-%m-%d %H:%M:%S')
    # 创建RotatingFileHandler对象,满1MB为一个文件，共备份3个文件
    log_file_handler = RotatingFileHandler(filename=r"log/bilibili.log",
                                           maxBytes=5 * 1024 * 1024,
                                           backupCount=3,
                                           encoding='utf-8')
    log_file_handler.setFormatter(formatter)
    logging.getLogger('my_logger').addHandler(log_file_handler)
    logger.info("Starting schedule...")

    create_database()

    # 每天10:13执行一次
    schedule.every().day.at("10:13", "Asia/Shanghai").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
