VERSION = "0.0.1"

all: build

build:
	@docker build -t bot:$(VERSION) -t bot:latest .

test:
	@docker-compose up -d

n ?= 10
train:
	python bot.py -t english
	python bot.py -t reddit
	n=$(n); \
	while [ $${n} -gt 0 ] ; do \
			echo $$n ; \
			python bot.py -t twitter; \
			sleep(60); \
			n=`expr $$n - 1`; \
	done; \
	true

.PHONY: all build test
