"""Communicate with the server."""
import json
import thread
import time
import websocket
import turk
import print_helpers as tp

LOCAL_TEST = True


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
    def run(*args):
        pass
    thread.start_new_thread(run, ())


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
