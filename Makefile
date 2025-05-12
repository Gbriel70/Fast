# Makefile for building and running a Docker container

#=======================BUILD========================#

build:
	docker build -t fast .

#=======================RUN=========================#

run:
	docker run -p 8080:8000 fast

#=======================BUILD AND RUN===============#

all: build run

#=======================TEST=======================#

test: build
	docker run -e PYTHONPATH=/app fast pytest

#=======================PHONY======================#

PHONY: build run build-run test