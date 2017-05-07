"""Example of how the camera works.

More docs here: https://picamera.readthedocs.io
"""
from picamera import PiCamera
from time import sleep


def take_a_picture(filepath="baby_charlie_sleeping.jpg",
                   exposure_mode='verylong',
                   iso=1600,
                   mode_or_iso="iso"):
    camera = PiCamera()

    camera.start_preview()
    sleep(2)
    camera.capture(filepath)
    camera.stop_preview()


if __name__ == "__main__":
    take_a_picture()
