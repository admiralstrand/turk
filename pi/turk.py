# -*- coding: utf-8 -*-
"""Mechanical Turk.

Code to make the turk's text input work
"""
import text_input_helpers as tt
import time
import math
try:  # ben's computer
    import ada1
except:
    import ben_shim as ada1

WIDE = 20
HIGH = 4

LIVEMODE = False
BACKSPACE_KEY = 127
ENTER_KEY = 13
CTRL_C = 3


def tappy_typing():
    """Get a single key press from the user, then push to LCD.

    Also handles special cases:
        ctrl+c to leave the programme.
        Enter to send
        backspace and arrow keys
    """
    acceptableChars = tt.get_acceptable_chars()

    print "\nWelcome to the turk"
    print "I accept:", acceptableChars
    print("start typing dood!")

    running_string = ""
    cursor_pos = 0
    while True:
        print("--------------------")
        typed_input = tt.get_char()
        print "input:", typed_input

        if typed_input in ["UP", "DOWN", "RIGHT", "LEFT"]:
            cursor_pos = tt.update_cursor_pos(typed_input,
                                              running_string,
                                              cursor_pos)
            cursor_pos = tt.clamp(cursor_pos, len(running_string))
            column = cursor_pos % WIDE
            row = int(math.floor(cursor_pos/WIDE))
            ada1.set_cursor(column, row)

        elif ord(typed_input) == CTRL_C:
            if not LIVEMODE:
                print "!! EJECT !! EJECT !! EJECT !!"
                yield "exit please"

        elif ord(typed_input) == ENTER_KEY:
            ada1.write_to_screen("Sending")
            time.sleep(0.5)
            ada1.write_to_screen("")
            # TODO: the actual sending code
            yield running_string
            running_string = ""

        elif tt.buffer_length(running_string) == 80:
            running_string = tt.send_complete_words(running_string)
            tt.show(running_string, cursor_pos)

        elif ord(typed_input) == BACKSPACE_KEY:
            running_string = tt.backspace(running_string)
            cursor_pos -= 1
            tt.show(running_string, cursor_pos)

        elif typed_input not in acceptableChars:
            print "don't be sketchy.\n{} not in {}".format(typed_input,
                                                           acceptableChars)

        else:
            temp_s_list = list(running_string)
            temp_s_list.insert(cursor_pos, typed_input)
            running_string = "".join(temp_s_list)
            cursor_pos += 1

        tt.show(running_string, cursor_pos)


if __name__ == "__main__":
    t = tappy_typing()
    next(t)
