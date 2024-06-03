SUDO := sudo

PIP := pip
PYTHON := python3.11

CURRENT_USER := $(shell whoami)
USER_DIR := /home/$(CURRENT_USER)
ROOT_DIR := /root

REQUIERMENTS_DIR := requirements
SRC_DIR := src

.DEFAULT_GOAL = help

.PHONY: setup-venv
setup-venv:
	$(PYTHON) -m venv .

.PHONY: setup
setup:
	$(SUDO) apt-get update
	$(PIP) install -r $(REQUIERMENTS_DIR)/requirements.txt
	$(PYTHON) setup.py build
	$(PYTHON) setup.py install

.PHONY: clean
clean:
	rm -rf bin \
		build \
		include \
		lib \
		lib64 \
		dist \

.PHONY: data-work

.PHONY: help
help:
	@echo "-------------------- USAGE --------------------"
	@echo ""
	@echo "setup"
	@echo "		Setup project, install requirements"
	@echo ""
	@echo "setup-venv"
	@echo "		Setup virtualenv in current directory"
	@echo ""
	@echo "clean"
	@echo "		Clean project"
	@echo ""
	@echo ""
