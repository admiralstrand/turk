# -*- coding: utf-8 -*-
"""Mechanical Turk text input functions."""
import string
import math
try:  # ben's computer
    import ada1
except:
    print "I think I'm running on Ben's computer"
    import ben_shim as ada1


def read_single_keypress():
    """Wait for a single keypress on stdin, then do something when it arrives.

    This is a silly function to call if you need to do it a lot because it has
    to store stdin's current setup, setup stdin for reading single keystrokes
    then read the single keystroke then revert stdin back after reading the
    keystroke.

    Returns the character of the key that was pressed (zero on
    KeyboardInterrupt which can happen when a signal gets handled)

    from http://stackoverflow.com/a/6599441/1835727 written by mheyman
    """
    import fcntl
    import os
    import sys
    import termios
    fd = sys.stdin.fileno()
    # save old state
    flags_save = fcntl.fcntl(fd, fcntl.F_GETFL)
    attrs_save = termios.tcgetattr(fd)
    # make raw - the way to do this comes from the termios(3) man page.
    attrs = list(attrs_save)  # copy the stored version to update
    # iflag
    attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK
                  | termios.ISTRIP | termios.INLCR | termios. IGNCR
                  | termios.ICRNL | termios.IXON)
    # oflag
    attrs[1] &= ~termios.OPOST
    # cflag
    attrs[2] &= ~(termios.CSIZE | termios. PARENB)
    attrs[2] |= termios.CS8
    # lflag
    attrs[3] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON
                  | termios.ISIG | termios.IEXTEN)
    termios.tcsetattr(fd, termios.TCSANOW, attrs)
    # turn off non-blocking
    fcntl.fcntl(fd, fcntl.F_SETFL, flags_save & ~os.O_NONBLOCK)
    # read a single keystroke
    try:
        ret = sys.stdin.read(1)  # returns a single character
    except KeyboardInterrupt:
        ret = 0
    finally:
        # restore old state
        termios.tcsetattr(fd, termios.TCSAFLUSH, attrs_save)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags_save)
    return ret


def get_acceptable_chars(special_chars=""):
    ur"""Return a string of acceptable characters to type.

    i.e.:
    0123456789 abcdefghijklmnopqrstuvwxyz
    ABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,
    -./:;<=>?@[\\]^_`{|}~

    add extra chars through the argument. E.g.
        get_acceptable_chars(special_chars="∞×¼")
    be aware that the system might not be able to handle these chars though!
    """
    numbers = "".join([str(i) for i in range(10)])
    letters = string.ascii_letters
    punctuation = string.punctuation
    acceptableChars = "".join([numbers,
                               " ",
                               special_chars,
                               letters,
                               punctuation])
    return acceptableChars


def hyphenate(word, max_width=20):
    """Extremely ghetto hyphenation.

    There must be a nice algoritm that's just out of reach of my brain today.
    """
    print len(word)
    if len(word) <= max_width:
        return word
    elif len(word) > 20 and len(word) <= 40:
        mid = int(math.floor(len(word)/2))
        print 1, mid, "<"
        return word[:mid] + " " + word[mid:]
    elif len(word) > 40 and len(word) <= 58:
        # 59 is hard to handle
        mid = int(math.floor(len(word)/3))
        print 2, mid, "<"
        return word[:mid] + " " + word[mid:mid*2] + " " + word[mid*2:]
    elif len(word) > 58:
        w = max_width
        print 3, w, "<"
        rtn = " ".join([word[:w], word[w:w*2], word[w*2:w*3], word[w*3:]])
        print rtn
        return rtn
    else:
        print "don't be a jerk"
        return word


def break_for_wide_x_high_screen(typed_input, wide=20, high=4):
    """Break up the typed input into lines."""
    screen = [""]
    row = 0
    words = typed_input.split()
    words = " ".join([hyphenate(x) for x in words]).split()
    print words
    for word in words:
        if len(screen[row]) + len(word) <= wide:
            screen[row] += (word + " ")
        else:
            row += 1
            screen.append("")
            screen[row] += (word + " ")

    screen += [''] * (4 - len(screen))  # fill in the blanks
    screen = [r.ljust(wide, " ") for r in screen]

    return screen


def prepare_for_screen(text, wide=20, high=4):
    """Convert the input list of lists to a string.

    also remove the trailing newline.
    """
    payload = ""
    for x in text:
        payload += x.strip().ljust(wide) + "\n"
    return payload.strip("\n")


def send_complete_words(running_string):
    """Send the characters up to the last space.

    Returns characters after the last space to be added to.
    """
    last_space = running_string.rfind(" ")
    print "SENDING", running_string[:last_space]
    # TODO: actually send
    return running_string[last_space:]


def backspace(running_string):
    """Pull the last char of the string."""
    length = len(running_string)
    return running_string[:length-1]


def buffer_length(running_text):
    """Measure the length of the broken up string."""
    as_list_of_lists = break_for_wide_x_high_screen(running_text)
    as_str = prepare_for_screen(as_list_of_lists)
    return len(as_str)


# if pretty_print:
#     for x in screen:
#         print "|"+x[0].strip().ljust(wide)+"|"
#     print "-" + "+" * (wide-1) + "-"
#     print len(typed_input), typed_input
#     print [len(x[0]) for x in screen], screen


def show(running_string):
    """Print to console and show on lcd."""
    screen_data = break_for_wide_x_high_screen(running_string)
    screen_data = prepare_for_screen(screen_data)
    ada1.write_to_screen(screen_data)
