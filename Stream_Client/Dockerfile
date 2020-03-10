FROM youreabosonharry/arm32v7_opencv4:0.1.0
LABEL maintainer="rath3.14159@protonmail.com"
RUN pip3 install grpcio grpcio-tools
WORKDIR /Stream_Client
COPY . .
ENTRYPOINT ["python3", "-u", "Stream_Client.py"]

