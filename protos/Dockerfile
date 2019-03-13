FROM python

RUN apt-get update -y --fix-missing
RUN apt-get install -y wget unzip libatomic1

WORKDIR /tmp/
RUN wget https://github.com/grpc/grpc-web/releases/download/1.0.3/protoc-gen-grpc-web-1.0.3-linux-x86_64
RUN mv protoc-gen-grpc-web-1.0.3-linux-x86_64 /usr/local/bin/protoc-gen-grpc-web
RUN chmod +x /usr/local/bin/protoc-gen-grpc-web

RUN wget https://github.com/protocolbuffers/protobuf/releases/download/v3.7.0/protoc-3.7.0-linux-x86_64.zip
RUN unzip protoc-3.7.0-linux-x86_64.zip
RUN cp -r include/* /usr/local/include/
RUN mv bin/protoc /usr/local/bin/
RUN chmod +x /usr/local/bin/protoc

RUN pip install --upgrade pip
RUN pip install grpcio-tools
