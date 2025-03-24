from flask import Flask, Response
import cv2
import threading
import time
from picamera2 import Picamera2

class Camera:

    def __init__(self):
        self.app = Flask(__name__)  # Initialize Flask app within the class
        self.picam2 = Picamera2()
        self.config = self.picam2.create_preview_configuration({"size": (640, 480)})
        self.picam2.configure(self.config)
        self.picam2.start()

        self.latest_frame = None
        self.frame_event = threading.Event()
        self.qr_code = None
        self.scan_enabled = True  # Default to scanning enabled

        # Initialize QR Code detector
        self.detector = cv2.QRCodeDetector()

        # Start the frame capture thread
        threading.Thread(target=self.capture_frames, daemon=True).start()

        # Define the Flask routes
        self.app.add_url_rule('/video_feed', 'video_feed', self.video_feed)
        self.app.add_url_rule('/qr_code', 'get_qr_code', self.get_qr_code)


    def capture_frames(self):
        while True:
            frame = self.picam2.capture_array()
            if frame is None:
                continue

            # QR Code detection
            data, bbox, _ = self.detector.detectAndDecode(frame)
            if bbox is not None and data:
                # QR code detected, store the data
                print("QR Code detected:", data)
                self.qr_code = data
                # Optionally, add the QR code data to the frame (e.g., display it)
                cv2.putText(frame, f"QR Code: {data}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            if ret:
                self.latest_frame = buffer.tobytes()
                self.frame_event.set()

            time.sleep(0.01)

    def generate_frames(self):
        while True:
            self.frame_event.wait()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + self.latest_frame + b'\r\n')
            self.frame_event.clear()

    def video_feed(self):
        return Response(self.generate_frames(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    def get_qr_code(self):
        if self.qr_code is not None:
            return self.qr_code 
        return None


# # Create an instance of CameraSingleton (this will start the Flask app as well)
# camera_instance = CameraSingleton()

# if __name__ == '__main__':
#     # Running the Flask app inside the singleton instance
#     camera_instance.app.run(host='0.0.0.0', port=8000, threaded=True)
