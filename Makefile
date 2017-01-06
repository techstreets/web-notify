IMAGE_NAME := techstreets/web-notify
IMAGE_TAG := 1.0.0
CONTAINER_NAME := web_notify
ENV_FILE_NAME := web_notify_env
HOST_PORT := 5001

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))

MAKE_DIR := $(strip $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST)))))

ifndef ${ENV_FILE_NAME}
	ifeq ($(shell test -s ./env && echo -n yes),yes)
		ENV_FILE := $(abspath ./env)
	else
		ENV_FILE := /dev/null
	endif
else
	ENV_FILE := ${${ENV_FILE_NAME}}
endif

.PHONY: all deploy build clean create deploy kill start stop restart shell docker_ip gen_secret

all: create deploy restart

build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

clean:
	docker images $(IMAGE_NAME) | grep -q $(IMAGE_TAG) && docker rmi $(IMAGE_NAME):$(IMAGE_TAG) || true

create:
	docker run --name $(CONTAINER_NAME) --restart=always --env-file $(ENV_FILE) -d -p $(HOST_PORT):80 -v $(MAKE_DIR):/opt/app $(IMAGE_NAME):$(IMAGE_TAG)

deploy:
	docker exec -it $(CONTAINER_NAME) pip install -r requirements.txt


kill:
	docker stop $(CONTAINER_NAME) && docker rm $(CONTAINER_NAME)

start:
	docker start $(CONTAINER_NAME)

stop:
	docker stop $(CONTAINER_NAME)

restart:
	docker restart $(CONTAINER_NAME)

shell:
	docker exec -it $(CONTAINER_NAME) bash

docker_ip:
	@ip addr show docker0 | grep "inet\b" | awk '{print $2}' | cut -d/ -f1

gen_secret:
	@python -c 'import random; print "".join([random.SystemRandom().choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])'
