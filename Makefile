AUTHOR?=dairlair
APP=mediagrabber

GIT_COMMIT:=$(shell git rev-parse --short HEAD)
GIT_UNTRACKED_CHANGES:=$(shell git status --porcelain --untracked-files=no)
ifneq ($(GIT_UNTRACKED_CHANGES),)
	GIT_COMMIT := $(GIT_COMMIT)-dirty
endif

RELEASE=$(GIT_COMMIT)

# Docker settings
DOCKER_REGISTRY?=docker.io
DOCKER_IMAGE?=${AUTHOR}/${APP}
DOCKER_REGISTRY_IMAGE=${DOCKER_REGISTRY}/${DOCKER_IMAGE}

.PHONY: image
image:
	docker build -t $(DOCKER_IMAGE):$(RELEASE) .
	docker tag $(DOCKER_IMAGE):$(RELEASE) $(DOCKER_IMAGE):latest

.PHONY: run
run: image
	docker run --env-file .env --rm --name=$(APP) $(DOCKER_IMAGE):latest

.PHONY: publish
publish: image
	docker push $(DOCKER_REGISTRY_IMAGE):$(RELEASE)
	docker push $(DOCKER_REGISTRY_IMAGE):latest

.PHONY: migrate
migrate:
	alembic upgrade head

.PHONY: remigrate
remigrate:
	alembic downgrade base && alembic upgrade head
