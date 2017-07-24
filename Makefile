COMPOSE_FILE ?= 'docker-compose.yml'
COMPOSE_CMD = docker-compose -f $(COMPOSE_FILE)

COMPOSE_RUN = $(COMPOSE_CMD) run --rm

up:
	$(COMPOSE_CMD) up -d

run-web:
	$(COMPOSE_RUN) web

build:
	$(COMPOSE_CMD) build

restart-db:
	$(COMPOSE_CMD) restart db

restart-web:
	$(COMPOSE_CMD) restart web

log-web:
	$(COMPOSE_CMD) logs --tail 10 -f web

log-db:
	$(COMPOSE_CMD) logs --tail 10 -f db
