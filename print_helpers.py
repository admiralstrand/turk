# -*- coding: utf-8 -*-
"""Mechanical Turk.

Code to make the turk's printer work

echo "This is a test." | lpr
or for image:
lpr -o fit-to-page /usr/share/raspberrypi-artwork/raspberry-pi-logo.png
"""
import cairo
import os
import rsvg
import text_input_helpers as tt


def naive_print(to_print):
    """Print text simply."""
    lines_list = tt.break_for_wide_x_high_screen(to_print)
    broken_string = tt.prepare_for_screen(lines_list)
    type_this = "echo \"{body}\" | lpr".format(body=broken_string)
    print "should be printing", type_this
    os.system(type_this)


def svg_print(text):
    """Print an image of some text derived from an SVG."""
    svg_string = svg_template(text)
    print svg_string
    img = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1000, 400)
    ctx = cairo.Context(img)
    # handle = rsvg.Handle(<svg filename>)
    # or, for in memory SVG data:
    handle = rsvg.Handle(None, svg_string)
    handle.render_cairo(ctx)
    img.write_to_png("tempPrint.png")
    try:
        type_this = "lpr -o orientation-requested=3 -o fit-to-page tempPrint.png"
        os.system(type_this)
        print "should be printing", type_this
    except Exception as e:
        print "probably on Ben's computer", e


def svg_template(text):
    """Provide an svg for the printer to print."""
    text = tt.break_for_wide_x_high_screen(text)
    # transform="matrix(-0.85988046,0,0,-0.85988046,1032.4181,384.69312)"
    template = u"""
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="400"
     xmlns:xlink="http://www.w3.org/1999/xlink">
  <g >
    <image width="1152" height="720" x="-63.4" y="-347.3"
           xlink:href="ben.png" transform="translate(50,200)"
           preserveAspectRatio="none"/>
    <text id="text1" x="100" y="100" font-size="90">{line1}</text>
    <text id="text2" x="100" y="200" font-size="90">{line2}</text>
    <text id="text3" x="100" y="300" font-size="90">{line3}</text>
    <text id="text4" x="100" y="400" font-size="90">{line4}</text>
  </g>
</svg>
"""
    return template.format(line1=text[0],
                           line2=text[1],
                           line3=text[2],
                           line4=text[3])


if __name__ == "__main__":
    svg_print("now is the time for all good turks to "
              "come to the aid of the mariocart")
