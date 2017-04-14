# -*- coding: utf-8 -*-
"""Testing for the Mechanical Turk."""

import text_input as t
import mock

A = ("1234567901234567901234567901234567901234"
     "56790123456790123456790123456790")
B = ("so, in general, I think it'd be easiest "
     "to: a) install the win 10 linux")
C = ("Now is the time for all good men to come"
     " to the aid of the party, quick or the beer will run out")


def test_get_acceptable_chars(special_chars=""):
    chars = ("0123456789 abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"
             "\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~")
    assert t.get_acceptable_chars(special_chars="") == chars


def test_break_for_wide_x_high_screen():
    expected = [['Now is the time for '],
                ['all good men to come '],
                ['to the aid of the '],
                ['party, quick or the '],
                ['beer will run out ']]

    assert t.break_for_wide_x_high_screen(C, wide=20, high=4) == expected


def test_prepare_for_screen(text, wide=20, high=4):
    expected = ('Now is the time for \n'
                'all good men to come\n'
                'to the aid of the   \n'
                'party, quick or the \n'
                'beer will run out')
    assert t.prepare_for_screen(text, wide=20, high=4) == expected


def test_send_complete_words():
    t.send_complete_words(running_string)


def test_backspace():
    given = ("Now is the time")
    expected = ("Now is the")
    backspaced = given
    for _ in range(5):
        backspaced = t.backspace(backspaced)

    assert backspaced == expected


def test_show():
    print "-" * 20
    t.show(C)
    print "-" * 20


def test_tappy_typing():
    """Simulate actually typing letters."""
    pass


if __name__ == '__main__':
    test_get_acceptable_chars(special_chars="")
    test_break_for_wide_x_high_screen()
    test_prepare_for_screen(t.break_for_wide_x_high_screen(C))
    # test_send_complete_words()
    test_backspace()
    test_show()
    # test_tappy_typing()
    # test_typing()
