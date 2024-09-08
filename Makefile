export WORKING_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
export APP_DIR := /states
export TOOLS_IMAGE := erikjseidel/python-tools
export PYLINTRC := /var/cache/.pylintrc
export MYPYRC := /var/cache/.mypy.ini

.PHONY: format
format:
	docker run --rm -v $(WORKING_DIR)/$(APP_DIR):$(APP_DIR)/ $(TOOLS_IMAGE) \
               black --fast --skip-string-normalization $(APP_DIR)/

.PHONY: black
black:
	docker run --rm -v $(WORKING_DIR)/$(APP_DIR):$(APP_DIR)/ $(TOOLS_IMAGE) \
               black --fast --skip-string-normalization --check $(APP_DIR)/

.PHONY: lint
lint:
	docker run --rm -v $(WORKING_DIR)/$(APP_DIR):$(APP_DIR)/ -v $(WORKING_DIR)/.pylintrc:$(PYLINTRC) -i $(TOOLS_IMAGE) \
               pylint --recursive=true --rcfile=$(PYLINTRC) $(APP_DIR)

.PHONY: type-check
type-check:
	docker run --rm -v $(WORKING_DIR)/$(APP_DIR):$(APP_DIR)/ -v $(WORKING_DIR)/.mypy.ini:$(MYPYRC) $(TOOLS_IMAGE) \
	       mypy -p _modules -p _runners -p _pillar -p _grains  --config-file $(MYPYRC)
