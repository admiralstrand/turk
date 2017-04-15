# -*- coding: utf-8 -*-
"""Mechanical Turk.

Code to make the turk's printer work

echo "This is a test." | lpr
or for image:
lpr -o fit-to-page /usr/share/raspberrypi-artwork/raspberry-pi-logo.png
"""
import os
import text_input_helpers as tt


def naive_print(to_print):
    lines_list = tt.break_for_wide_x_high_screen(to_print)
    broken_string = tt.prepare_for_screen(lines_list)
    type_this = "echo \"{body}\" | lpr".format(body=broken_string)
    print "should be printing", type_this
    os.system(type_this)
