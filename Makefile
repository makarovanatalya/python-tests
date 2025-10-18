IMAGE_NAME ?= unat9/python-test
TEST_PROFILE ?= api
TEST_OUTPUT_DIR = logs/$(shell date +"%Y%_m_%d_%H_%M%_S")

# docker image

.PHONY: build-docker-container
build-docker-container:
	$(info $(M) going to build docker container with tests)
	docker build -t $(IMAGE_NAME) .

.PHONY: run-docker-container
run-docker-container:
	$(info $(M) going to run docker container with tests)
	mkdir -p $(TEST_OUTPUT_DIR)
	docker run --rm \
		   -v $(shell pwd)/$(TEST_OUTPUT_DIR):/app/logs \
		   -e TEST_PROFILE=$(TEST_PROFILE) -e SERVER=http://host.docker.internal:4111/api -e UI_BASE_URL=http://host.docker.internal:3000 \
           -t $(IMAGE_NAME)
	$(info $(M) tests finished, check results in $(TEST_OUTPUT_DIR))

.PHONY: publish-docker-container
publish-docker-container:
	docker push $(IMAGE_NAME)
