# -*- coding: utf-8 -*-
"""Mechanical Turk.

Spoof the ada library
"""
import math
import text_input_helpers as tt


def write_to_screen(thing, cursor_pos=None, wide=20, high=4):
    """Pretend to write to screen, actually just print."""
    lines_of_text = thing.split("\n")
    right_edge = list("|" * 4)
    top_row = "-" * 20

    if cursor_pos:
        cursor_pos = tt.clamp(cursor_pos, wide * high)
        column = cursor_pos % wide
        row = int(math.floor(cursor_pos/wide))
        row = tt.clamp(row, 3)  # 80/4 is 4, but 0123 rows - overflow
        top_row = top_row[:cursor_pos-1] + "|" + top_row[cursor_pos:]
        set_cursor(column, row)
        right_edge[row] = "<-"
    print "|" + top_row
    for i, line in enumerate(lines_of_text):
        print "|" + line + right_edge[i]


def set_cursor(col, row):
    """Pretend to set the cursor position."""
    print row, ",", col
