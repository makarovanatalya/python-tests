DOCKER_USER ?=
DOCKER_PASSWORD ?=
IMAGE_NAME = $(DOCKER_USER)/python-test
TAG = latest

DOCKER_COMPOSE_FILE = infra/docker-compose/docker-compose.yml

TEST_OUTPUT_DIR ?= test-results/$(shell date +"%Y%_m_%d_%H_%M")
SERVER ?= http://localhost:4111/api
UI_BASE_URL ?= http://localhost:3000

# DOCKER IMAGE
.PHONY: build-docker-container
build-docker-container:
	@echo "going to build docker container with tests"
	docker buildx create --use
	docker buildx build --platform linux/amd64,linux/arm64 -t $(IMAGE_NAME):$(TAG) .

.PHONY: run-docker-container
run-docker-container:
	@echo "going to run docker container with tests"
	mkdir -p $(TEST_OUTPUT_DIR)
	docker run --rm --name test-runner \
		   --platform linux/amd64 \
		   --network host \
		   -v $(shell pwd)/$(TEST_OUTPUT_DIR)/allure-results:/app/allure-results \
		   -e SERVER=$(SERVER) -e UI_BASE_URL=$(UI_BASE_URL) \
           $(IMAGE_NAME):$(TAG)
	@echo "tests finished, check results in $(TEST_OUTPUT_DIR)"

.PHONY: publish-docker-container
publish-docker-container:
	echo $(DOCKER_PASSWORD) | docker login -u $(DOCKER_USER) --password-stdin
	docker buildx build --push --platform linux/amd64,linux/arm64 -t $(IMAGE_NAME):$(TAG) .

# DOCKER COMPOSE
.PHONY: stop-app
stop-app:
	docker compose -f $(DOCKER_COMPOSE_FILE) down

.PHONY: start-app
start-app:
	make stop-app
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d

# RUN TESTS
.PHONY: run-tests
run-tests:
	pytest -v --log-level=DEBUG --log-cli-level=DEBUG --alluredir allure-results