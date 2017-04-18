"""Communicate with the server."""
import json
import thread
import time
import websocket
import turk
import print_helpers as tp


def on_message(ws, message):
    message = json.loads(message)
    print "*"*10, "\n\nmessage", message, "\n"
    if message["handle"] == "turkBrain":
        # TODO: add styled printing
        tp.svg_print(message["text"])
    elif message["handle"] == "turkClient":
        # TODO: add styled printing
        tp.svg_print(message["text"])
    else:
        print "someone else is on the system!\n{}".format(message)


def on_error(ws, error):
    print "error", error


def on_close(ws):
    print "### closed ###"


def on_open(ws):
    def run(*args):
        print "here we go"
        t = turk.tappy_typing()
        while True:
            # time.sleep(1)
            value = next(t)
            if value != "exit please":
                payload = json.dumps({"handle": "turk",
                                      "text": value})
            else:
                break
            print "dump", payload
            ws.send(payload)
        time.sleep(1)
        # ws.close()
        # print "thread terminating..."
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    # server_address = "wss://echo.websocket.org"
    # server_address = "ws://localhost:5000/echo"
    # server_address = ("ws://ec2-52-40-215-205.us-west-2.compute."
    #                   "amazonaws.com/echo")
    server_address = "ws://nameless-dusk-67549.herokuapp.com/submit"
    # server_address = "ws://localhost:5000/submit"
    ws = websocket.WebSocketApp(server_address,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
