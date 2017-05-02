"""Communicate with the server."""
import json
import sys
import thread
import time
import websocket
from turk import tappy_typing
from print_helpers import svg_print
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish


def on_connect(client,userdata,flags,rc):
    global topic
    global server_address
    global port
    print("connected : " + str(rc))
    client.subscribe(topic)
    publish.single(topic, payload ="connected!", hostname=server_address, port=port)
    #run(topic,port,server_address)
    thread.start_new_thread(run,(topic,port,server_address))

def on_message(client,userdata,msg):
    """Print incoming message.

    Listen to the redis PUBSUB. When a message is received,
    print it to the recipt printer.

    TODO: use a different template depending on who the message is from.
    """
    print str(msg.payload)
    if (msg):
        message =str(msg.payload)
        message = json.loads(message)
        print message
        print_message_nicely(message)
        if message["handle"] == "turkBrain":
            svg_print(message["text"], sender="turkBrain")
        elif message["handle"] == "turkClient":
            svg_print(message["text"], sender="turkClient")
        else:
            print "someone else is on the system!\n{}".format(message)

def run(topic,port,server_address):
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
        publish.single(topic, payload =payload, hostname=server_address, port=port)
    time.sleep(1)

def print_message_nicely(message):
    """Print a message in a nice way."""
    print ("\n\r" + "*"*10 + "\n" +
           "\rsender:  " + message["handle"] + "\n" +
           "\rmessage: " + message["text"] + "\n\r" +
           "*"*10 + "\n")


if __name__ == "__main__":

    if sys.argv[1] == "local":
        server_address = "localhost"
        port=5000
    else:
        server_address = 'test.mosca.io'
        port = 1883

    topic = 'mqtest'

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(server_address,port)
    client.loop_forever()
