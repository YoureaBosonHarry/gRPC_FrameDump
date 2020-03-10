import cv2
import grpc
import logging
import os
import time
import video_server_pb2
import video_server_pb2_grpc

# Configure Logging
logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.INFO)

# Environment Variables
FRAME_RATE = int(os.environ.get("FRAMERATE", 3))
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")

def send_frames():
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    time.sleep(2)
    while 1:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        yield video_server_pb2.FrameInfo(image=bytes(gray))
        time.sleep(float(1/FRAME_RATE))

def main():
    channel = grpc.insecure_channel(f'{HOST}:{PORT}')
    stub = video_server_pb2_grpc.FrameServiceStub(channel)
    stub.DumpFrame(send_frames())

if __name__ == '__main__':
    main()
