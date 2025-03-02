FROM python:3.12.8-alpine3.21

LABEL authors="Orange Summer"

WORKDIR ./bilibili_follow_LRU

ADD . .

RUN pip install -r requirements.txt

RUN pip install pytz

CMD ["python", "./src/main.py"]