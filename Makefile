VERSION = "0.0.1"

all: build

build:
	@docker build -t bot:$(VERSION) -t bot:latest .

test: build
	@docker-compose down
	@docker-compose up -d

deploy: build
	@docker stack deploy -c docker-compose-stack.yml edward

destroy:
	@docker stack rm edward
	@docker-compose down

n ?= 10
train:
	python edward.py -t english
	python edward.py -t reddit
	n=$(n); \
	while [ $${n} -gt 0 ] ; do \
			echo $$n ; \
			python edward.py -t twitter; \
			sleep 60; \
			n=`expr $$n - 1`; \
	done; \
	true

.PHONY: all build test deploy destroy train
