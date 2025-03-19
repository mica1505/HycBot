from picamzero import Camera
import os

home_dir = os.environ['HOME'] #set the location of your home directory
cam = Camera()

cam.start_preview()
cam.take_photo(f"{home_dir}/Desktop/new_image.jpg") #save the picture
cam.record_video(f"{home_dir}/Desktop/new_video.mp4", duration=5)
cam.stop_preview()