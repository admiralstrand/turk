"""Communicate with the server."""
import json
import thread
import time
import websocket
from turk import tappy_typing
from print_helpers import svg_print

LOCAL_TEST = True


def on_message(ws, message):
    """Print incoming message.

    Listen to the redis PUBSUB. When a message is received,
    print it to the recipt printer.

    TODO: use a different template depending on who the message is from.
    """
    message = json.loads(message)
    print_message_nicely(message)
    if message["handle"] == "turkBrain":
        svg_print(message["text"], sender="turkBrain")
    elif message["handle"] == "turkClient":
        svg_print(message["text"], sender="turkClient")
    else:
        print "someone else is on the system!\n{}".format(message)


def on_error(ws, error):
    """Print the error if it occurs."""
    print "error", error


def on_close(ws):
    """Do things when the connection closes."""
    print "### closed ###"


def on_open(ws):
    """Maintain a connection to the server.

    `tappy_typing()` is a generator. It gets input from the user. When
    the user is happy with their message, they press enter and it is
    yielded back to this function. This function then formats the message
    as JSON, adds a sender tag, and sends it off to the server.

    The server then puts it into the redis pubsub and sends it to the web
    client and back to here for the printer (see on_message).
    """
    def run(*args):
        t = tappy_typing()
        while True:
            value = next(t)
            if value != "exit please":
                payload = json.dumps({"handle": "turkClient",
                                      "text": value})
            else:
                ws.close()
                print "thread terminating..."
                return True
            print "dump", payload
            ws.send(payload)
        time.sleep(1)
    thread.start_new_thread(run, ())


def listen(ws):
    """Open a connection to the redis channel."""
    def run(*args):
        pass
    thread.start_new_thread(run, ())


def print_message_nicely(message):
    """Print a message in a nice way."""
    print "\n" + "*"*10
    print "sender:", message["handle"]
    print message["text"]
    print "*"*10, "\n"


if __name__ == "__main__":
    websocket.enableTrace(True)
    if LOCAL_TEST:
        server_address = "ws://localhost:5000"
    else:
        server_address = "ws://nameless-dusk-67549.herokuapp.com/submit"

    in_ws = websocket.WebSocketApp(server_address + "/receive",
                                   on_message=on_message,
                                   on_error=on_error,
                                   on_close=on_close)
    in_ws.on_open = listen
    thread.start_new_thread(in_ws.run_forever, ())

    out_ws = websocket.WebSocketApp(server_address + "/submit",
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
    out_ws.on_open = on_open
    out_ws.run_forever()
