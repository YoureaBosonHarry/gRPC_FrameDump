FROM arm32v7/python:3.8-buster
LABEL maintainer="rath3.14159@protonmail.com"
RUN pip3 install grpcio grpcio-tools
WORKDIR /Frame_Dump
COPY . .
ENTRYPOINT ["python3", "-u", "Frame_Dump.py"]
