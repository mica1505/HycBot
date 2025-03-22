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
    # Create a QR code detector once
    qr_detector = cv2.QRCodeDetector()
    
    while True:
        # Capture a frame from the camera
        frame = picam2.capture_array()
        if frame is None:
            continue

        # Draw a small "X" at the center
        height, width = frame.shape[:2]
        center_x, center_y = width // 2, height // 2
        offset = 10  # Small size for the "X"
        cv2.line(frame,
                 (center_x - offset, center_y - offset),
                 (center_x + offset, center_y + offset),
                 (0, 255, 0), 2)
        cv2.line(frame,
                 (center_x - offset, center_y + offset),
                 (center_x + offset, center_y - offset),
                 (0, 255, 0), 2)

        # --- QR Code Detection ---
        try:
            data, bbox, _ = qr_detector.detectAndDecode(frame)
        except cv2.error as e:
            data, bbox = "", None

        if bbox is not None and data:
            # Draw a blue contour around the QR code
            n = len(bbox)
            for i in range(n):
                pt1 = tuple(bbox[i][0].astype(int))
                pt2 = tuple(bbox[(i + 1) % n][0].astype(int))
                cv2.line(frame, pt1, pt2, (255, 0, 0), 2)
            # Put the decoded text above the center X
            cv2.putText(frame, data, (center_x - offset, center_y - offset - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            print("QR Code detected:", data)

        # --- Black Box Detection ---
        # Convert frame to grayscale and threshold to find dark regions.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # THRESH_BINARY_INV: dark areas become white; adjust threshold as needed (here 50)
        _, mask = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
        # Find contours in the thresholded image
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            # Filter out small regions to reduce noise
            if area > 500:
                x, y, w, h = cv2.boundingRect(cnt)
                # Draw a red rectangle around the detected black box
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                # Calculate and draw the centroid of the black box
                cx = int(x + w / 2)
                cy = int(y + h / 2)
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                cv2.putText(frame, "Robot", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Encode the frame as JPEG (quality 80 for a good balance)
        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        if ret:
            latest_frame = buffer.tobytes()
            frame_event.set()

        # Small pause to ease CPU usage
        time.sleep(0.01)

# Start frame capture in a background thread
threading.Thread(target=capture_frames, daemon=True).start()

def generate_frames():
    while True:
        frame_event.wait()  # Wait until a new frame is available
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + latest_frame + b'\r\n')
        frame_event.clear()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Run the app on port 8000, accessible on the network
    app.run(host='0.0.0.0', port=8000, threaded=True)
