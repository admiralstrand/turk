# -*- coding: utf-8 -*-
"""Mechanical Turk.

Code to make the turk's text input work
"""
import text_input_helpers as tt
import time
import math
# import sys
try:  # ben's computer
    # if sys.argv[1] == "local":
    #     import ben_shim as ada1
    # else:
    #     print "using the real driver"
    #     import ada1
    import ada1

except:
    import ben_shim as ada1

WIDE = 20
HIGH = 4

LIVEMODE = True
BACKSPACE_KEY = 127
ENTER_KEY = 13
CTRL_C = 3

SEND_PAUSE = 1.5  # seconds
blank3rows = (((" "*20)+"\n")*3)


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
    cursor_pos = 1
    while True:
        typed_input = tt.get_char()
        # print "input:", typed_input

        if typed_input in ["UP", "DOWN", "RIGHT", "LEFT"]:
            cursor_pos = tt.update_cursor_pos(typed_input,
                                              running_string,
                                              cursor_pos)
            cursor_pos = tt.clamp(cursor_pos, len(running_string)+1)
            column = cursor_pos % WIDE
            row = int(math.floor(cursor_pos/WIDE))
            ada1.set_cursor(column, row)

        elif typed_input is None:
            print "got an f key probably"

        elif ord(typed_input) == CTRL_C:
            if not LIVEMODE:
                print "!! EJECT !! EJECT !! EJECT !!"
                yield "exit please"
            else:
                print "Someone is trying to kill me, but I'm invincible"

        elif ord(typed_input) == ENTER_KEY:
            ada1.write_to_screen("Sending...")
            time.sleep(SEND_PAUSE)
            ada1.write_to_screen("")
            yield running_string
            running_string = ""

        elif ord(typed_input) == BACKSPACE_KEY:
            running_string = tt.backspace(running_string[:80], cursor_pos)
            cursor_pos -= 1

        elif typed_input not in acceptableChars:
            print "don't be sketchy.\n{} not in {}".format(typed_input,
                                                           acceptableChars)

        else:
            bl = tt.buffer_length(running_string)
            if bl >= 75:
                print "fat buffy"
                ada1.write_to_screen(blank3rows + "Running out of space")
                time.sleep(0.2)
                tt.show(running_string, cursor_pos)
            elif bl >= 79:
                ada1.write_to_screen(blank3rows + "        Out of space")
                time.sleep(0.5)
                tt.show(running_string, cursor_pos)
            trim = 80
            if bl > 80:
                trim = 79 - bl

            running_string = running_string[:trim]
            temp_s_list = list(running_string)
            temp_s_list.insert(cursor_pos, typed_input)
            running_string = "".join(temp_s_list)
            cursor_pos += 1
            cursor_pos = tt.clamp(cursor_pos, 80)
            print "adding", typed_input

        tt.show(running_string, cursor_pos)


if __name__ == "__main__":
    t = tappy_typing()
    next(t)
