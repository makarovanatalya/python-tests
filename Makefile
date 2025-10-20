DOCKER_USER = unat9
DOCKER_PASSWORD ?= 
IMAGE_NAME = $(DOCKER_USER)/python-test
TAG = latest
TEST_PROFILE ?= api
TEST_OUTPUT_DIR = test-results/$(shell date +"%Y%_m_%d_%H_%M")
DOCKER_COMPOSE_FILE = infra/docker-compose/docker-compose.yml
SERVER ?= http://host.docker.internal:4111/api
UI_BASE_URL ?= http://host.docker.internal:80

# DOCKER IMAGE SECTION
.PHONY: build-docker-container
build-docker-container:
	@echo "going to build docker container with tests"
	docker buildx create --use
	docker buildx build --platform linux/amd64,linux/arm64 -t $(IMAGE_NAME):$(TAG) .

.PHONY: run-docker-container
run-docker-container:
	@echo "going to run docker container with tests"
	mkdir -p $(TEST_OUTPUT_DIR)
	docker run --rm \
		   --platform linux/amd64 \
		   -v $(shell pwd)/$(TEST_OUTPUT_DIR)/logs:/app/logs \
		   -e TEST_PROFILE=$(TEST_PROFILE) -e SERVER=$(SERVER) -e UI_BASE_URL=$(UI_BASE_URL) \
           $(IMAGE_NAME):$(TAG)
	@echo "tests finished, check results in $(TEST_OUTPUT_DIR)"

.PHONY: publish-docker-container
publish-docker-container:
	echo $(DOCKER_PASSWORD) | docker login -u $(DOCKER_USER) --password-stdin
	docker buildx build --push --platform linux/amd64,linux/arm64 -t $(IMAGE_NAME):$(TAG) .

# DOCKER COMPOSE SECTION
.PHONY: start-app
start-app:
	docker compose -f $(DOCKER_COMPOSE_FILE) down
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d
