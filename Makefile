# ================================================================
# Makefile — azure-openai-poc
# ================================================================

APP_NAME = azure-openai-poc
TAG ?= latest
PORT ?= 5001

.PHONY: help build run shell logs clean

help:
	@echo "Commandes disponibles :"
	@echo "  make build   -> build l'image Docker"
	@echo "  make run     -> lance le conteneur"
	@echo "  make shell   -> shell dans le conteneur"
	@echo "  make logs    -> logs du conteneur"
	@echo "  make clean   -> supprime l'image Docker"

build:
	docker build -t $(APP_NAME):$(TAG) .

run:
	docker run --rm -it \
		--env-file .env \
		-p $(PORT):5000 \
		$(APP_NAME):$(TAG)

shell:
	docker run --rm -it --env-file .env $(APP_NAME):$(TAG) bash

logs:
	docker logs -f $(APP_NAME) || true

clean:
	docker rmi -f $(APP_NAME):$(TAG) || true
