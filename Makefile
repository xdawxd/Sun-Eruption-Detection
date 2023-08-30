IMAGE_TAG = "sun_eruption_detection"

# Poetry commands

poetry-install:
	poetry install

poetry-update:
	poetry update

# Linters
lint:
	black . && ruff --fix .

mypy-check:
	mypy .

# Docker
build:
	docker build --tag $(IMAGE_TAG) .

run:
	docker run $(IMAGE_TAG)

bash:
	docker exec -it $(IMAGE_TAG) /bin/bash

