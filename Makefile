VERSION = "0.1.1"

all: build

build:
	@docker build -t wgill/bot:$(VERSION) -t wgill/bot:latest .

push: build
	@docker push wgill/bot:latest

test: build
	@docker-compose down
	@docker-compose up -d

deploy: build, push
	@docker stack deploy -c docker-compose-stack.yml edward

destroy:
	@docker stack rm edward
	@docker-compose down

n ?= 5
train:
	@python edward.py -t english
	@python edward.py -t reddit
	n=$(n); \
	while [ $${n} -gt 0 ] ; do \
			echo $$n ; \
			python edward.py -t twitter; \
			sleep 60; \
			n=`expr $$n - 1`; \
	done; \
	true

export:
	@mongoexport -d bot_db -c statements > export.json

docs:
	@./docs.sh
	@git add README.md
	@git commit -m "update"
	@git push

.PHONY: all build test deploy destroy train
