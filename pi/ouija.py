#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Communicate with the server."""
import json
import sys
import thread
import time
import math
from turk import tappy_typing
from print_helpers import svg_print
from print_helpers import print_pic
from print_helpers import print_remote_pic
try:
    from camera import take_a_picture
except:
    from ben_shim import take_a_picture
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# cam globals
iso = 200
exposure_mode = 'verylong'
mode_or_iso = "iso"
brightness = 50
# print globals
print_direction = 1  # TODO: make this make sense
# roll globals
print_counter = 0
roll_length = 15000  # value in mm, but really, who cares.
each_print_length = 120  # value in mm, but really, who cares.
number_of_prints_before_end_to_warn = 8


def remote_command(message):
    """Respond to commands from the brain.

    This allows for the brain to set commands on the pi, remotely.

    e.g. from the interface
        settings (can be any or all of the k:v pairs)
            /set|iso:1600,exposure_mode:night,mode_or_iso:iso,print_direction:1,brightness:50
        take a picture
            /picture
            /pic
            /photo
        print a picture
            /pp
            /print pic
            /print picture
        print a picture from the web
            /webpic
            /wp
    """
    m = message.split("|")
    if m[0][0] != "/":
        print "something not right, command called with a non command", message
        raise
    if m[0] in ["/pp", "/print pic", "/print picture"]:
        print_pic()
    if m[0] in ["/wp", "/webpic"]:
        print_remote_pic(m[1])
    if m[0] in ["/roll", "/new roll"]:
        global print_counter
        print_counter = 0
    if m[0] in ["/set", "/settings"]:
        global brightness
        global exposure_mode
        global iso
        global mode_or_iso
        global print_direction
        global roll_length
        global each_print_length
        if len(m) > 1:
            pairs = m[1].split(",")
            for pair in pairs:
                p = pair.split(":")
                if p[0] == "iso":
                    iso = int(p[1])
                if p[0] == "exposure_mode":
                    exposure_mode = p[1]
                if p[0] == "mode_or_iso":
                    mode_or_iso = p[1]
                if p[0] == "print_direction":
                    print_direction = p[1]
                if p[0] == "brightness":
                    brightness = p[1]
                if p[0] == "roll_length":
                    roll_length = p[1]
                if p[0] == "each_print_length":
                    each_print_length = p[1]
        print "settings requested:", m[0]
        print "settings now:"
        print "iso {}, exposure_mode {}, mode_or_iso {}".format(iso,
                                                                exposure_mode,
                                                                mode_or_iso)
    if m[0] in ["/photo", "/pic", "/picture"]:
        print "taking a pic with settings:"
        print "iso {}, exposure_mode {}, mode_or_iso {}".format(iso,
                                                                exposure_mode,
                                                                mode_or_iso)
        take_a_picture(filepath="live.jpg",
                       exposure_mode=exposure_mode,
                       iso=iso,
                       mode_or_iso=mode_or_iso)


def on_connect(client, userdata, flags, rc):
    """Handle connection."""
    global topic
    global server_address
    global port
    print("connected : " + str(rc))
    client.subscribe(topic)
    publish.single(topic,
                   payload="connected!",
                   hostname=server_address,
                   port=port)
    # run(topic,port,server_address)
    thread.start_new_thread(run, (topic, port, server_address))


def on_message(client, userdata, msg):
    """Print incoming message."""
    # print str(msg.payload)
    if (msg):
        message = str(msg.payload)
        try:
            message = json.loads(message)
        except ValueError:
            message = {"text": message,
                       "handle": "turkBrain"}
        except Exception as e:
            print e
        print_message_nicely(message)
        if message["handle"] == "turkBrain":
            if message["text"][0] == "/":
                remote_command(message["text"])
            else:
                svg_print(message["text"],
                          sender="turkBrain",
                          direction=print_direction)
        elif message["handle"] == "turkClient":
            svg_print(message["text"],
                      sender="turkClient",
                      direction=print_direction)
        else:
            print "someone else is on the system!\n{}".format(message)
        print "\n\rwaiting for more input:\r"


def run(topic, port, server_address):
    """Run the session.

    tappy_typing is a generator, it hands control over to the input code when
    it's running then the generator hands it back with a message.
    """
    global print_counter
    number_of_prints_on_this_roll = math.floor(roll_length / each_print_length)
    t = tappy_typing()
    while True:
        value = next(t)
        print "taking a pic with settings:"
        print "iso {}, exposure_mode {}, mode_or_iso {}".format(iso,
                                                                exposure_mode,
                                                                mode_or_iso)
        take_a_picture(filepath="live.jpg",  # values from globals
                       exposure_mode=exposure_mode,
                       iso=iso,
                       mode_or_iso=mode_or_iso)
        if value != "exit please":
            payload = json.dumps({"handle": "turkClient",
                                  "text": value})
            print "dump", payload
            publish.single(topic,
                           payload=payload,
                           hostname=server_address,
                           port=port)
        else:
            # ws.close()
            print "thread terminating..."
            return True

        print_counter += 1
        m = "{} of {} prints left on this roll"
        print m.format(int(number_of_prints_on_this_roll - print_counter),
                       int(number_of_prints_on_this_roll))
        if print_counter == (number_of_prints_on_this_roll -
                             number_of_prints_before_end_to_warn):
            paper_warning = ("Please warn my human helper that my paper "
                             "is running low or I will be silenced.")
            publish.single(topic,
                           payload=paper_warning,
                           hostname=server_address,
                           port=port)

    time.sleep(1)


def print_message_nicely(message):
    """Print a message in a nice way."""
    print ("\n\r" + "*"*10 + "\n" +
           "\rsender:  " + message["handle"] + "\n" +
           "\rmessage: " + message["text"] + "\n\r" +
           "*"*10 + "\n")


if __name__ == "__main__":
    try:
        if sys.argv[1] == "local":
            server_address = "localhost"
            port = 5000
    except:
        print "Running live (or at least trying)."
        server_address = 'test.mosca.io'
        port = 1883

    topic = 'mqtest'

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(server_address, port)
    client.loop_forever()
