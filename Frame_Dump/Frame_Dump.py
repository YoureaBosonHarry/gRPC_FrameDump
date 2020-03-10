from concurrent import futures
import grpc
import logging
import os
import time
import video_server_pb2
import video_server_pb2_grpc

# Environment Variables
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")

logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.DEBUG)

class FrameDumpServicer(video_server_pb2_grpc.FrameServiceServicer):
    def __init__(self, max_frames):
        self.frames = []
        self.max_frames = max_frames

    def DumpFrame(self, request_iterator, context):
       for i in request_iterator:
           self.push_to_dump(i)
       return video_server_pb2.FrameResponse(reply="OK")

    def push_to_dump(self, frame):
        self.frames.append(frame)
        if len(self.frames) >= self.max_frames:
            self.frames.pop(0)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    video_server_pb2_grpc.add_FrameServiceServicer_to_server(FrameDumpServicer(50), server)
    server.add_insecure_port(f'{HOST}:{PORT}')
    logging.info(f"Starting Server On Port {PORT}")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
  serve()
