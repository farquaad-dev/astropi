import util

from io import BytesIO
from picamera import PiCamera
from PIL import Image
from time import sleep
from datetime import datetime

camera = PiCamera()
camera.resolution = (1296,972)
stream = BytesIO()

def capture(debug_capture=False):
    camera.start_preview()
    sleep(2)
    camera.capture(stream, 'png')
    stream.seek(0)
    img =  Image.open(stream)

    if debug_capture:
        img.save(util.path_for(f'debug-img-{datetime.now()}.png'))

    stream.seek(0)
    return img
