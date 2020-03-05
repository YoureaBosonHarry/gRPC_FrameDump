ARG VERSION=0.1.0
FROM youreabosonharry/arm32v7_opencv4:0.1.0
LABEL maintainer="rath3.14159@protonmail.com"
WORKDIR /Stream_Client
COPY . .
RUN pip3 install grpcio grpcio-tools
ENTRYPOINT ["python3", "-u", "Stream_Client.py"]

