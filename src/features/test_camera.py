import os
import cv2
import numpy as np
import threading
import gi
import subprocess

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

# Initialisation de GStreamer
Gst.init(None)


def start_gstreamer_stream(host, port):
    """Démarre un stream vidéo en utilisant GStreamer sans rpicamsrc."""
    pipeline = Gst.parse_launch(
        f"v4l2src device=/dev/video0 ! video/x-raw, width=640, height=480, format=YUY2 ! videoconvert ! x264enc tune=zerolatency bitrate=500 ! rtph264pay config-interval=1 pt=96 ! gdppay ! udpsink host={host} port={port} sync=false"
    )
    pipeline.set_state(Gst.State.PLAYING)
    return pipeline


def stop_gstreamer_stream(pipeline):
    """Arrête le pipeline GStreamer."""
    pipeline.set_state(Gst.State.NULL)

def start_video_stream():
    """Lit le flux vidéo et tente de détecter un QR Code en temps réel."""
    cap = cv2.VideoCapture(
        "udpsrc port=5000 ! gdpdepay ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink sync=false",
        cv2.CAP_GSTREAMER
    )
    if not cap.isOpened():
        print("Erreur : Impossible d'ouvrir le flux vidéo.")
        return
    
    detector = cv2.QRCodeDetector()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur : Impossible de lire la vidéo.")
            continue
        
        # Détection du QR Code
        data, bbox, _ = detector.detectAndDecode(frame)
        if bbox is not None:
            for i in range(len(bbox)):
                cv2.line(frame, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), (0, 255, 0), 2)
            if data:
                print(f"QR Code détecté : {data}")
                cv2.putText(frame, data, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow('Streaming Video', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def main():
    host = "192.168.1.145"
    port = 5000
    
    print("Démarrage du streaming...")
    pipeline = start_gstreamer_stream(host, port)
    
    try:
        start_video_stream()
    except KeyboardInterrupt:
        print("Arrêt du streaming...")
    finally:
        stop_gstreamer_stream(pipeline)

if __name__ == "__main__":
    main()
