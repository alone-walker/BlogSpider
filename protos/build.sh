#! /usr/bin/env bash


SPIDER_PATH="$(pwd)/../"
NAME="grpc"

if !(docker image ls --format '{{.Repository}}' | grep -q "$NAME"); then
	docker image build -t $NAME .
fi

docker container run --rm -v ${SPIDER_PATH}/protos/:/protos/ -v ${SPIDER_PATH}/spider:/spider/ -v ${SPIDER_PATH}/www/:/www/ -w /protos/ grpc ./grpc-protos.sh
