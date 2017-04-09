# -*- coding: utf-8 -*-
"""Testing for the Mechanical Turk."""

import text_input as t


def test_line_breaking():
    """Test to see if the line breaks work properly.

    TODO: remove print code from the actual function, move it here.
    """
    a = ("1234567901234567901234567901234567901234"
         "56790123456790123456790123456790")
    b = ("so, in general, I think it'd be easiest "
         "to: a) install the win 10 linux")
    c = ("Now is the time for all good men to come"
         " to the aid of the party quick")

    t.break_for_80x20_screen(a)
    t.break_for_80x20_screen(b)
    t.break_for_80x20_screen(c)


if __name__ == '__main__':
    test_line_breaking()
