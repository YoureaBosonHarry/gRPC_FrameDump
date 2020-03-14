import cv2
import grpc
import video_server_pb2
import video_server_pb2_grpc
import Motion_Detector

HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")

def detect_motion(stub, frame_count, accumulated_weight=0.1, width=400, height=400):
    global frames
    motion_detector = Motion_Detector.FrameMotionDetector(accumulated_weight)
    total = 0
    while True:
        frame = stub.ReturnFrame(video_server_pb2.FrameResponse.reply = "OK")
        if frames:
            img = frames.pop(0)
            # Convert Bytes to Numpy Array For OpenCV
            frame = np.frombuffer(img, dtype=np.uint8)
            # Downscale And Apply Gaussian Blur
            gray = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
            cv2.imshow('image', gray)
            gray = cv2.GaussianBlur(gray, (7, 7), 0)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if total > frame_count:
                # Check for motion in frames
                motion = motion_detector.detect(gray, threshold_val=motion_threshold)
                if motion is not None:
                    print("motion detected")
            # Update Current Background
            motion_detector.update(gray)
            total += 1

def main():
    channel = grpc.insecure_channel(f'{HOST}:{PORT}')
    stub = video_server_pb2_grpc.FrameServiceStub(channel)
    detect_motion(stub, 3)

if __name__ == '__main__':
    main()
