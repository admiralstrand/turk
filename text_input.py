# -*- coding: utf-8 -*-
"""Mechanical Turk.

Code to make the turk's text input work
"""
import string
import ada1
LIVEMODE = False


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
    print numbers, letters, punctuation
    acceptableChars = "".join([numbers,
                               " ",
                               special_chars,
                               letters,
                               punctuation])
    return acceptableChars


def break_for_wide_x_high_screen(typed_input,
                                 wide=20,
                                 high=4,
                                 pretty_print=True):
    """Break up the typed input into lines.

    TODO: make it break long words etc. Unlikely to be needed any time soon.
    """
    screen = [[""]]
    row = 0
    for word in typed_input.split():
        if len(screen[row][0]) + len(word) <= wide:
            screen[row][0] += (word + " ")
        else:
            row += 1
            screen.append([""])
            screen[row][0] += (word + " ")

    if pretty_print:
        for x in screen:
            print "|"+x[0].strip().ljust(wide)+"|"
        print "-" + "+" * (wide-1) + "-"
        print len(typed_input), typed_input
        print [len(x[0]) for x in screen], screen

    return screen.strip("\n")


def prepare_for_screen(text, wide=20, high=4):
    payload = ""
    for x in text:
        payload += x[0].strip().ljust(wide) + "\n"
    return payload


def tappy_typing():
    """Get a single key press from the user, then push to LCD.

    This handles special cases, like ctrl+c to leave the programme.
    """
    acceptableChars = get_acceptable_chars()
    print "I accept:", acceptableChars

    while True:
        running_string = ""
        ada1.write_to_screen(message="your wish is my bumhole")
        print("start typing dood!")
        while True:  # len(running_string) < 20:
            print("next letter:")
            typed_input = read_single_keypress()
            if ord(typed_input) == 3:  # 3 is ctrl + c. Dissable in live
                if not LIVEMODE:
                    print "EJECT!!EJECT!!EJECT!!"
                    return True
            elif ord(typed_input) == 13:
                print "SENDING"
                # TODO: the actual sending code
                running_string = ""
            elif ord(typed_input) == 127:  # backspace
                length = len(running_string)
                running_string = running_string[:length-1]
                screen_data = break_for_wide_x_high_screen(running_string)
            else:
                if typed_input not in acceptableChars:
                    print "don't be a sketchy fuck"
                else:
                    running_string += typed_input
                    # add in a line here that says something like
                    screen_data = break_for_wide_x_high_screen(running_string)
            screen_data = prepare_for_screen(screen_data)
            ada1.write_to_screen(screen_data)


if __name__ == "__main__":
    tappy_typing()
