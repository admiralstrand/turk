# -*- coding: utf-8 -*-
"""Mechanical Turk.

Code to make the turk's printer work

echo "This is a test." | lpr
or for image:
lpr -o fit-to-page /usr/share/raspberrypi-artwork/raspberry-pi-logo.png
"""
from shutil import copyfile
import cairo
import datetime
import os
import requests
import rsvg
import text_input_helpers as tt

WIDTH = 1000
HEIGHT = 1000


def naive_print(to_print):
    """Print text simply."""
    lines_list = tt.break_for_wide_x_high_screen(to_print)
    broken_string = tt.prepare_for_screen(lines_list)
    type_this = "echo \"{body}\" | lpr".format(body=broken_string)
    print "should be printing", type_this
    os.system(type_this)


def print_pic():
    """Print the last picture taken."""
    type_this = ("lpr "
                 "-o orientation-requested=4 "
                 "-o fit-to-page "
                 "live.jpg")
    os.system(type_this)
    file_name = "history/{}.jpg".format(timestamp())
    copyfile("live.jpg", file_name)
    log("printed " + file_name)


def timestamp():
    """Return a string timestamp."""
    a = datetime.datetime.utcnow()
    return a.strftime("%Y-%m-%d_%H:%M")


def log(message):
    """Add to the log of what was said and printed."""
    history_book = open("history/log.txt", "a")
    history_book.write("\n{}:  {}".format(timestamp(), message))
    history_book.close()


def print_remote_pic(url):
    """Get an image from the internet and print it."""
    page = requests.get(url)
    with open('live.jpg', 'wb') as test:
        test.write(page.content)
    print_pic()


def svg_print(text,
              sender=None,
              chatty=False,
              save_svg=True,
              direction=1):
    """Print an image of some text derived from an SVG.

    Take an SVG template and inject the text into it.
    Save that SVG as a PNG.
    Print the PNG to the recipt printer using a bash command.
    """
    svg_string = ""
    if sender == "turkBrain":
        print "printing as turkBrain:\n"
        svg_string = brain_svg(text)
        log("turkBrain:   {}".format(text))
    elif sender == "turkClient":
        print "printing as turkClient:\n"
        svg_string = client_svg(text)
        log("turkClient:  {}".format(text))
    else:
        svg_string = svg_template(text)
    if chatty:
        print svg_string

    img = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(img)
    handle = rsvg.Handle(None, svg_string)
    handle.render_cairo(ctx)
    if save_svg:
        svg_file = open(sender + ".svg", 'w')
        svg_file.write(svg_string)
        svg_file.close()
    img.write_to_png("tempPrint.png")
    try:
        type_this = ("lpr "
                     "-o orientation-requested=" + str(direction) + " "
                     "-o fit-to-page "
                     "tempPrint.png")
        os.system(type_this)
        print "should be printing:\n", type_this
    except Exception as e:
        print "probably on Ben's computer", e


def brain_svg(text):
    """Return the SVG template suitable for the aAI's voice."""
    # TODO: add styled printing
    return svg_template(text, font="Ceria Lebaran", font_size=150)


def client_svg(text):
    """Return the SVG template suitable for the client's voice."""
    # TODO: add styled printing
    return svg_template(text, font="Martienso", font_size=170)


def plain_svg(text):
    """Return the SVG template for when no voice is passed in."""
    # TODO: add styled printing
    return svg_template(text)


def svg_template(text, font="", font_size=90, stroke="silver", fill="none"):
    """Provide an svg for the printer to print."""
    text = tt.break_for_wide_x_high_screen(text)
    template = u"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"
     xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="a">
      <rect width="1000" height="1000" x="0" y="0"/>
    </clipPath>
  </defs>
  <rect x="0" y="0" width="1000" height="400"
        fill="{fill}" stroke="{stroke}" stroke-width="3" />
  <rect x="0" y="400" width="1000" height="600"
        fill="{fill}" stroke="{stroke}" stroke-width="3" />
  <g transform="matrix(-0.85988046,0,0,-0.85988046,1032.4181,384.69312)">
    <text x="60" y="100" font-size="{font_size}"
          font-family="{font}">{line1}</text>
    <text x="60" y="200" font-size="{font_size}"
          font-family="{font}">{line2}</text>
    <text x="60" y="300" font-size="{font_size}"
          font-family="{font}">{line3}</text>
    <text x="60" y="400" font-size="{font_size}"
          font-family="{font}">{line4}</text>
  </g>
</svg>
"""
    return template.format(line1=text[0],
                           line2=text[1],
                           line3=text[2],
                           line4=text[3],
                           font=font,
                           font_size=font_size,
                           w=WIDTH,
                           h=HEIGHT,
                           stroke=stroke,
                           fill=fill)


if __name__ == "__main__":
    import sample
    import random
    st = sample.sample_text
    r = random.randint(0, len(st)-80)
    st = st[r:r+80]
    t = ("now is the time for "
         "all good turks to "
         "come to the aid of "
         "the mariocart")
    w = ("WWWWWWWWWWWWWWWWWWW"
         "WWWWWWWWWWWWWWWWWWW"
         "WWWWWWWWWWWWWWWWWWW"
         "WWWWWWWWWWWWWWWWWWW")
    tc = "turkClient"
    tb = "turkBrain"

    svg_print(st,
              sender=tc,
              chatty=True,
              save_svg=True,
              direction=1)

    print_remote_pic("http://digitalpolyphony.webs.com/billandted2.jpg")
