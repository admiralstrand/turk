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


def svg_print(text, sender=None, chatty=False, save_svg=True):
    """Print an image of some text derived from an SVG.

    Take an SVG template and inject the text into it.
    Save that SVG as a PNG.
    Print the PNG to the recipt printer using a bash command.
    """
    svg_string = ""
    if sender == "turkBrain":
        svg_string = brain_svg(text)
    elif sender == "turkClient":
        svg_string = client_svg(text)
    else:
        svg_string = svg_template(text)
    if chatty:
        print svg_string

    img = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1000, 400)
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
                     "-o orientation-requested=3 "
                     "-o fit-to-page "
                     "tempPrint.png")
        os.system(type_this)
        print "should be printing:\n", type_this
    except Exception as e:
        print "probably on Ben's computer", e


def brain_svg(text):
    """Return the SVG template suitable for the aAI's voice."""
    # TODO: add styled printing
    return svg_template(text, font="Ceria Lebaran", font_size=90)


def client_svg(text):
    """Return the SVG template suitable for the client's voice."""
    # TODO: add styled printing
    return svg_template(text, font="Martienso", font_size=130)


def plain_svg(text):
    """Return the SVG template for when no voice is passed in."""
    # TODO: add styled printing
    return svg_template(text)


def svg_template(text, font="", font_size=90):
    """Provide an svg for the printer to print."""
    text = tt.break_for_wide_x_high_screen(text)
    template = u"""
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="400"
     xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="a">
      <rect width="1000" height="400" x="0" y="0"/>
    </clipPath>
  </defs>
  <rect x="0" y="0" width="1000" height="400" fill="none" stroke="red" stroke-width="3" />
  <g transform="matrix(-0.85988046,0,0,-0.85988046,1032.4181,384.69312)">
    <image width="1152" height="720" x="-63.4" y="-347.3"
           xlink:href="ben.png" transform="translate(50,200)"
           clip-path="url(#a)" preserveAspectRatio="none"/>
    <text x="60" y="100" font-size="{font_size}" font-family="{font}">{line1}</text>
    <text x="60" y="200" font-size="{font_size}" font-family="{font}">{line2}</text>
    <text x="60" y="300" font-size="{font_size}" font-family="{font}">{line3}</text>
    <text x="60" y="400" font-size="{font_size}" font-family="{font}">{line4}</text>
  </g>
</svg>
"""
    return template.format(line1=text[0],
                           line2=text[1],
                           line3=text[2],
                           line4=text[3],
                           font=font,
                           font_size=font_size)


if __name__ == "__main__":
    svg_print("now is the time for all good turks to "
              "come to the aid of the mariocart")
