import cv2
import grpc
import numpy as np
import os
import time
import video_server_pb2
import video_server_pb2_grpc
import Motion_Detector

HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")
THRESHOLD = int(os.environ.get("THRESHOLD", 40))
FRAME_RATE = int(os.environ.get("FRAME_RATE", 3))

def detect_motion(stub, frame_count, accumulated_weight=0.1, width=400, height=400):
    motion_detector = Motion_Detector.FrameMotionDetector(accumulated_weight)
    total = 0
    while True:
        response = video_server_pb2.FrameResponse(reply='OK')
        frame = stub.ReturnFrame(response)
        if frame:
            img = frame.image
            # Convert Bytes to Numpy Array For OpenCV
            frame = np.frombuffer(img, dtype=np.uint8)
            # Downscale And Apply Gaussian Blur
            gray = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
            gray = cv2.GaussianBlur(gray, (7, 7), 0)
            if total > frame_count:
                # Check for motion in frames
                motion = motion_detector.detect(gray, threshold_val=THRESHOLD)
                if motion is not None and np.sum(motion) != 0:
                    print("motion detected")
            # Update Current Background
            motion_detector.update(gray)
            total += 1
        time.sleep(1 / FRAME_RATE)

def main():
    print("Start")
    channel = grpc.insecure_channel(f'{HOST}:{PORT}')
    stub = video_server_pb2_grpc.FrameServiceStub(channel)
    print("Here")
    detect_motion(stub, 3)

if __name__ == '__main__':
    main()
