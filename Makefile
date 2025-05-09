# Makefile for building and running a Docker container

#=======================BUILD========================#

build:
	docker build -t fast .

#=======================RUN=========================#

run:
	docker run -p 8080:8080 fast

#=======================BUILD AND RUN===============#

all: build run

PHONY: build run build-run test