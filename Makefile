include ./make/print.lib.mk
include ./make/dynamic-recipe.lib.mk

#------------------------------
# dynamic recipes
#
# marked with # dynamic
# A named recipe (eg. manage) will set CMD, and call it
# if it's the last recipe being called (eg. make manage).
# A recipe caught by .DEFAULT will add the recipe name
# (eg. changepassword) to a list of ARGS, and call CMD with
# the list of ARGS if it's the last recipe being called
# (eg. make manage changepassword youruser).
#
# NOTE: don't create any recipes with the same name as any
#       dynamic recipe args (eg. changepassword)
#------------------------------

#------------------------------
# vars
#------------------------------

SHELL := /bin/bash
CMD := ""
POS_ARGS := ""
ARGS := ""
FILE_PATH_DOCKER_COMPOSE_LOCAL :=docker-compose.yml

#------------------------------
# helpers
#------------------------------

COMMA := ,

#------------------------------
# help
#------------------------------

.PHONY: help
help:
	$(call print_h1,"AVAILABLE","OPTIONS")
	$(call print_space)
	$(call print_h2,"docker")
	$(call print_h3,"add 'local' to build$(COMMA) up or buildup (eg. 'buildup local')$(COMMA) to run with '$(FILE_PATH_DOCKER_COMPOSE_LOCAL)'")
	$(call print_options,"build","Build docker containers for dev.")
	$(call print_options,"up","Launch all containers including api in http://localhost:4070.")
	$(call print_options,"buildup","Rebuild and launch all containers including api in http://localhost:4070.")
	$(call print_options,"stop","Clean code and stop any docker container.")
	$(call print_options,"destroy","Clean code and destroy docker processes$(COMMA) images and volumes.")
	$(call print_options,"destroy-all","Destroy docker processes$(COMMA) images and volumes.")
	$(call print_options,"down","Clean code and destroy docker processes.")
	$(call print_options,"pull","Download docker images in parallel.")
	$(call print_space)
	$(call print_h2,"utility")
	$(call print_options,"shell","Connect to the shell inside the api container.")
	$(call print_options,"shell-db","Connect to the shell inside the Postgres container.")
	$(call print_options,"shell-redis","Connect to the shell inside the Redis container.")
	$(call print_options,"clean","Remove all compiled files$(COMMA) coverage. 'sudo' maybe needed.")
	$(call print_space)
	$(call print_h2,"data")
	$(call print_options,"seed-database","Seed database from seed data files.")
	$(call print_space)
	$(call print_h2,"dependency")
	$(call print_options,"pip-compile","Compile requirements.txt from requirements.in and build the images for the api service.")
	$(call print_options,"pip-compile-upgrade","Compile requirements.txt from requirements.in upgrading the packages and build the images for the api service.")	
	$(call print_space)
	$(call print_h2,"Q&A")
	$(call print_options,"test","Run all tests.")
	$(call print_options,"pytest","Run all pytests.")
	$(call print_options,"pytest-h","Show pytest help")
	$(call print_options,"pytest","Run pytests (takes args additional via ARGS=\"...\" eg. \`\`make pytest ARGS=\"tests/unit/ --reuse-db\"\`\` or \`\`make pytest ARGS=\"-m \'mark1 and not mark2\'\"\`\`).")
	$(call print_options,"pytest-k","Run pytests by keyword eg. \`\`make pytest-k test_my_serializer`` (takes additional args via ARGS=\"...\" as above).")
	$(call print_space)
	$(call print_h2,"dynamic recipes")
	$(call print_h3,"accepts any number of additional positional args as well as --args via ARGS=\"...\"")

#------------------------------
# docker helpers
#------------------------------

# runs docker compose with the provided args,
# and prints out the full command being run
define dockercompose
	$(call print,"docker-compose $(1)")
	@docker-compose $(1)
endef

# checks for 'local' command and if local config file exists,
# and if so runs docker-compose using the local file,
# if not prints a warning and runs with default config.
define dockercomposelocal
	@$(eval TARGETING_LOCAL := $(if $(filter-out local,$(lastword $(MAKECMDGOALS))),,""))
	@$(eval LOCAL_FILE_EXISTS := $(if $(wildcard $(FILE_PATH_DOCKER_COMPOSE_LOCAL)),"",))
	@$(eval DOCKER_COMPOSE_FILE_ARG := $(if $(and $(TARGETING_LOCAL),$(LOCAL_FILE_EXISTS)),"-f $(FILE_PATH_DOCKER_COMPOSE_LOCAL) ",))
	@$(if $(TARGETING_LOCAL),$(if $(LOCAL_FILE_EXISTS),,$(call print_warning,"Local config missing$(COMMA) please create: $(FILE_PATH_DOCKER_COMPOSE_LOCAL)$(COMMA) using default...")),)
	$(call dockercompose,"$(DOCKER_COMPOSE_FILE_ARG)$(1)")
endef

#------------------------------
# docker
#------------------------------

.PHONY: local
local:
	@echo -n

.PHONY: build
build: pull
	$(call print_h1,"BUILDING","CONTAINERS")
	$(call dockercomposelocal,"build")
	$(call print_h1,"CONTAINERS","BUILT")

.PHONY: up
up:
	$(call print_h1,"LAUNCHING","ALL","DOCKER","CONTAINERS")
	$(call dockercomposelocal,"up")

.PHONY: buildup
buildup:
	$(call print_h1,"REBUILDING","AND","LAUNCHING","DOCKER CONTAINERS")
	$(call dockercomposelocal,"up --build")

.PHONY: stop
stop: clean
	$(call print_h1,"EXECUTING","DOCKER STOP")
	@-docker-compose stop
	@-docker stop `docker ps -aq`
	$(call print_h1,"DOCKER STOP","COMPLETE")

.PHONY: down
down: full-clean
	$(call print_h1,"EXECUTING","DOCKER DOWN")
	@-docker-compose down
	@-docker stop `docker ps -aq`
	@-docker rm `docker ps -aq`
	$(call print_h1,"DOCKER DOWN","COMPLETE")

.PHONY: destroy
destroy: full-clean
	$(call print_h1,"EXECUTING","DOCKER DESTROY")
	@-docker-compose down
	@-docker stop `docker ps -aq`
	@-docker rm `docker ps -aq`
	@-docker volume rm -f `docker volume ls -q`
	$(call print_h1,"DOCKER DESTROY","COMPLETE")

.PHONY: destroy-all
destroy-all: destroy
	$(call print_h1,"EXECUTING","DOCKER DESTROY","ALL","IMAGES")
	@-docker rmi --force `docker images -a -q`
	$(call print_h1,"DOCKER DESTROY","ALL","IMAGES","COMPLETE")

.PHONY: pull
pull:
	$(call print_h1,"DOWNLOADING","DOCKER","IMAGES")
	@docker-compose pull --parallel
	$(call print_h1,"DOCKER","IMAGES","DOWNLOADED")

#------------------------------
# utility
#------------------------------

.PHONY: shell
shell:
	$(call print_h1,"ENTERING","API","SHELL")
	@docker-compose run --rm api sh

.PHONY: shell-db
shell-db:
	$(call print_h1,"ENTERING","POSTGRES","SHELL")
	@docker-compose run --rm postgres sh

.PHONY: shell-redis
shell-redis:
	$(call print_h1,"ENTERING","REDIS","SHELL")
	@docker-compose run --rm redis sh

.PHONY: clean
clean:
	$(call print_h1,"EXECUTING","CLEAN")

	$(call print,"cleaning python files...")

	@-find . -name '*.egg-info' -exec rm -rf {} +
	@-find . -name '*.egg' -exec rm -f {} +
	@-find . -name '*.pyc' -exec rm -f {} +
	@-find . -name '*.pyo' -exec rm -f {} +
	@-find . -name '__pycache__' -exec rm -rf {} +

	$(call print,"cleaning test files...")

	@-rm -rf .cache
	@-rm -f .coverage
	$(call print_h1,"CLEANING","COMPLETE")

#------------------------------
# data
#------------------------------

.PHONY: seed_database
seed_database:
	$(call print_h1,"SEED DATA")
	@-docker-compose run --rm api flask seed-database
	$(call print_h1,"SEED DATA", "PREPARED")

#------------------------------
# dependency
#------------------------------

.PHONY: pip-compile
pip-compile:
	$(call print_h1,"COMPILING","API","REQUIREMENTS")
	@-docker-compose build api
	@-docker-compose run --rm api sh -c "pip-compile && sed -ri 's/^-e //' requirements.txt"
	@-docker-compose build api
	$(call print_h1,"API","REQUIREMENTS","COMPILED")

.PHONY: pip-compile-upgrade
pip-compile-upgrade:
	$(call print_h1,"COMPILING","AND","UPGRADING","API","REQUIREMENTS")
	@-docker-compose build api
	@-docker-compose run --rm api sh -c "pip-compile --upgrade && sed -ri 's/^-e //' requirements.txt"
	@-docker-compose build api
	$(call print_h1,"API","REQUIREMENTS","COMPILED","AND","UPGRADED")

#------------------------------
# Q&A
#------------------------------

.PHONY: test
test:
	$(call print_h1,"RUNNING","ALL","TESTS")
	@.circleci/test.sh api
	$(call print_h1,"ALL","TESTS","COMPLETE")

.PHONY: pytest
pytest:
	$(call print_h1,"RUNNING","PYTEST","TESTS")
	@docker-compose run --rm api pytest
	$(call print_h1,"PYTEST","TESTS","RUN")

.PHONY: pytest-h
pytest-h:
	$(call print_h1,"SHOWING","PYTEST","HELP")
	@docker-compose run --rm api pytest --help

#------------------------------
# dynamic functionality
#------------------------------

# adds recipe name (eg. changepassword) to POS_ARGS, calls CMD with ARGS and POS_ARGS if last
.DEFAULT:
	@$(eval POS_ARGS += $@)
	@$(eval ARGS += $(ARGS))
	$(call run_if_last,${CMD} ${ARGS} ${POS_ARGS})
