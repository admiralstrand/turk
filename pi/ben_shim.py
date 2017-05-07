# -*- coding: utf-8 -*-
"""Mechanical Turk.

Spoof the ada library
"""
import text_input_helpers as tt


def write_to_screen(thing, cursor_pos=None, wide=20, high=4):
    """Pretend to write to screen, actually just print."""
    tt.preview(thing, cursor_pos, wide, high)


def set_cursor(col, row):
    """Pretend to set the cursor position."""
    # print "cursor:", row, ",", col
    pass


def take_a_picture(*args, **kwargs):
    """Spoof taking a picture."""
    print "taking a picture (but not really)", args, kwargs
