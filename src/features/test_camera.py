from flask import Flask, Response
from picamera2 import Picamera2
import cv2
import threading
import time

app = Flask(__name__)

# Configure the camera in preview mode for better performance
picam2 = Picamera2()
config = picam2.create_preview_configuration({"size": (640, 480)})
picam2.configure(config)
picam2.start()

latest_frame = None
frame_event = threading.Event()

def capture_frames():
    global latest_frame
    detector = cv2.QRCodeDetector()
    while True:
        frame = picam2.capture_array()
        if frame is None:
            continue

        # Draw a small "X" at the center
        height, width = frame.shape[:2]
        center_x, center_y = width // 2, height // 2
        offset = 10  # Size of the "X"
        cv2.line(frame,
                 (center_x - offset, center_y - offset),
                 (center_x + offset, center_y + offset),
                 (0, 255, 0), 2)
        cv2.line(frame,
                 (center_x - offset, center_y + offset),
                 (center_x + offset, center_y - offset),
                 (0, 255, 0), 2)

        # Attempt QR code detection, handling any potential errors
        try:
            data, bbox, _ = detector.detectAndDecode(frame)
        except cv2.error as e:
            # If an error occurs, ignore QR detection for this frame
            data, bbox = "", None

        if bbox is not None and data:
            # Draw a blue contour around the QR code
            n = len(bbox)
            for i in range(n):
                pt1 = tuple(bbox[i][0].astype(int))
                pt2 = tuple(bbox[(i + 1) % n][0].astype(int))
                cv2.line(frame, pt1, pt2, (255, 0, 0), 2)
            # Display the decoded text
            cv2.putText(frame, data, (center_x - offset, center_y - offset - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            print("QR Code detected:", data)

        # Encode the frame as JPEG (quality 80 for a good compromise)
        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        if ret:
            latest_frame = buffer.tobytes()
            frame_event.set()

        # Small pause to reduce CPU load
        time.sleep(0.01)

# Start frame capture in a background thread
threading.Thread(target=capture_frames, daemon=True).start()

def generate_frames():
    while True:
        frame_event.wait()  # Wait for a new frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + latest_frame + b'\r\n')
        frame_event.clear()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True)
