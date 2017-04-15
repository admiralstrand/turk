# -*- coding: utf-8 -*-
"""Mechanical Turk.

Code to make the turk's text input work
"""
import print_helpers as tp
import text_input_helpers as tt
import time
try:  # ben's computer
    import ada1
except:
    print "I think I'm running on Ben's computer"
    import ben_shim as ada1

LIVEMODE = False
BACKSPACE_KEY = 127
ENTER_KEY = 13
CTRL_C = 3


def tappy_typing():
    """Get a single key press from the user, then push to LCD.

    This handles special cases, like ctrl+c to leave the programme.
    """
    acceptableChars = tt.get_acceptable_chars()

    print "\nWelcome to the turk"
    print "I accept:", acceptableChars
    print("start typing dood!")

    running_string = ""
    while True:
        print("--------------------")
        typed_input = tt.read_single_keypress()

        if ord(typed_input) == CTRL_C:
            if not LIVEMODE:
                print "!! EJECT !! EJECT !! EJECT !!"
                return True

        elif ord(typed_input) == ENTER_KEY:
            tp.svg_print(running_string)
            # TODO: the actual sending code
            running_string = ""
            ada1.write_to_screen("Sending")
            time.sleep(0.5)
            ada1.write_to_screen("")

        elif tt.buffer_length(running_string) == 80:
            running_string = tt.send_complete_words(running_string)
            tt.show(running_string)

        elif ord(typed_input) == BACKSPACE_KEY:
            running_string = tt.backspace(running_string)
            tt.show(running_string)

        elif typed_input not in acceptableChars:
            print "don't be a sketchy fuck"

        else:
            running_string += typed_input
            tt.show(running_string)


if __name__ == "__main__":
    tappy_typing()
