FROM python
MAINTAINER jahrik <jahrik@gmail.com>

COPY . /src/
WORKDIR /src

RUN pip install -r requirements.txt
