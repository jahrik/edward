FROM python:3.7.0a1-stretch
MAINTAINER jahrik <jahrik@gmail.com>
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y cron

RUN apt-get install -y jack

# python3_pyaudio deps
RUN apt-get install -y \
      libasound-dev \
      portaudio19-dev \
      libportaudio2 \
      libportaudiocpp0 \
      ffmpeg \
      libav-tools 

RUN apt-get install -y python3-pyaudio

RUN service cron start

WORKDIR /src
COPY edward.py /src
COPY requirements.txt /src
COPY config /src
COPY Makefile /src
COPY crontab /etc/cron.d/bot_cron

RUN pip install -r requirements.txt

CMD ["python3","edward.py","-b","gitter"]
