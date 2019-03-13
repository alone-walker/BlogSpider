#! /usr/bin/env bash


python3 -m grpc_tools.protoc -I. --python_out=/www/src/ --grpc_python_out=/www/src/ spider.proto
python3 -m grpc_tools.protoc -I. --python_out=/spider/src/ --grpc_python_out=/spider/src/ spider.proto
protoc -I=. --js_out=import_style=commonjs:/www/src/static/app/ --grpc-web_out=import_style=commonjs,mode=grpcwebtext:/www/src/static/app/ spider.proto
