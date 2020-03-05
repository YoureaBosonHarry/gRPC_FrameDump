import grpc
import video_server_pb2
import video_server_pb2_grpc
from concurrent import futures
import os
import time

class FrameDump(video_server_pb2_grpc.FrameServiceServicer):
    def __init__(self):
        self.frames = []

    def DumpFrame(self, request, context):
       for i in request:
           yield video_server_pb2.FrameResponse(reply="OK")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    video_server_pb2_grpc.add_FrameServiceServicer_to_server(FrameDump(), server)
    server.add_insecure_port('[::]:50051')
    print("Starting Server On Port: 50051")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
  serve()
