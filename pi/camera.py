"""Example of how the camera works.

More docs here: https://picamera.readthedocs.io
"""
from picamera import PiCamera
from time import sleep


def take_a_picture(filepath="baby_charlie_sleeping.jpg",
                   exposure_mode='verylong',
                   iso=1600,
                   mode_or_iso="iso"):
    """Take a picture."""
    camera = PiCamera()
    sleep(1)
    if mode_or_iso == "mode":
        camera.exposure_mode = exposure_mode
    elif mode_or_iso == "iso":
        camera.iso = iso
    # camera.start_preview()
    camera.capture(filepath)
    # camera.stop_preview()
    camera.close()


if __name__ == "__main__":
    take_a_picture()
