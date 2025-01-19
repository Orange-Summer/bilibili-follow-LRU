import asyncio
import telegram

from read_configuration import read_configuration


def send_message(content):
    chat_id, token = read_configuration('telegram_chat_id', 'telegram_bot_token')
    # 创建一个Bot对象，并传入API令牌
    bot = telegram.Bot(token=token)

    # 发送消息给指定的用户或群组
    asyncio.run(bot.send_message(chat_id=chat_id, text=content))
