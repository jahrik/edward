FROM python:3.7.0a1-stretch
MAINTAINER jahrik <jahrik@gmail.com>

RUN apt-get update
RUN apt-get install -y cron
RUN service cron start

WORKDIR /src
COPY edward.py /src
COPY requirements.txt /src
COPY config /src
COPY Makefile /src
COPY crontab /etc/cron.d/bot_cron

RUN pip install -r requirements.txt

CMD ["python3","edward.py","-t","gitter"]
