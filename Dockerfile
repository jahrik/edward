FROM python:3.7.0a1-stretch
MAINTAINER jahrik <jahrik@gmail.com>

WORKDIR /src
COPY bot.py /src
COPY requirements.txt /src
COPY config /src
COPY Makefile /src
COPY crontab /etc/cron.d/bot_cron
# RUN chmod 0744 /etc/cron.d/bot_cron

RUN pip install -r requirements.txt

CMD ["python3","bot.py","-t","gitter"]
