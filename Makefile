.PHONY: help

KERNEL_NAME := $(shell uname -s)
ifeq ($(KERNEL_NAME),Linux)
    OPEN := xdg-open
else ifeq ($(KERNEL_NAME),Darwin)
    OPEN := open
else
    $(error unsupported system: $(KERNEL_NAME))
endif

help: ## Print this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

setup: ## Install dependencies
	pip install -r requirements.txt
	pip install -r requirements.dev.txt

run: ## Run the server in development mode
	FLASK_APP=app.app:app flask run

test:
	pytest tests --cov-report term --cov=app

coverage: ## Opens html test coverage report in standard browser
	pytest tests --cov-report term --cov=app --cov-report html
	$(OPEN) htmlcov/index.html