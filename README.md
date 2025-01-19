# bilibili-follow-LRU

统计 Bilibili 长时间未观看的关注的 up 主，定时通过 telegram bot 发送消息。

目前只统计并通知一个月和三个月未观看的 up 主，需要程序保持运行一直读取观看历史记录并更新关注 up 主的最新观看时间。

## 运行方式

### 1. 建立映射路径

在宿主机建立两个文件夹分别用于映射容器中的 config 和 log 文件夹

在这两个文件夹参考项目分别新建 config.yaml 和 bilibili.log

### 2. 配置 config.yaml

config.yaml需要修改以下参数:

- `cookie`: b站的 cookie
- `User-Agent`: 自己浏览器的 User-Agent
- `user_id`: b站自己的用户 id
- `telegram_bot_token`: 使用[@BotFather](https://t.me/BotFather)创建 bot 得到的 token
- `telegram_chat_id`: 创建一个 channel 或者 group，将新建的 bot 拉进去，参考下述方法获取 chat id
  https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id

### 3. 构建镜像并运行容器

#### 修改 docker-compose.yml

修改 docker-compose.yml 中的 volumes 参数的宿主机路径为步骤一创建的文件夹

#### 在 Dockerfile 目录下执行以下命令

```bash
docker-compose up -d
```

## 修改通知时间

参考 [schedule库文档](https://schedule.readthedocs.io/)修改 main.py 中的下述代码

```python
schedule.every().day.at("10:13", "Asia/Shanghai").do(job)
```

## 注意事项

cookie 会失效，注意经常更换 config.yaml 中的 cookie 值