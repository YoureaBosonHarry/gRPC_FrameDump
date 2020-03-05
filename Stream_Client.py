import cv2
import grpc
import video_server_pb2
import video_server_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')

cap = cv2.VideoCapture(0)
def SendFrame(self, request, context):
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        yield video_server_pb2.FrameInfo(image=bytes(gray))

def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = imageTest_pb2_grpc.ImageTestStub(channel)
    stub.FrameDump(SendFrame())

if __name__ == '__main__':
    main()