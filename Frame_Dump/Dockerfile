ARG VERSION=0.1.0
FROM arm32v7/ubuntu:19.10
LABEL maintainer="rath3.14159@protonmail.com"
WORKDIR /Frame_Dump
COPY . .
RUN pip3 install grpcio grpcio-tools
ENTRYPOINT ["python3", "-u", "Frame_Dump.py"]
