#!/usr/bin/python 

import argparse
import mosquitto
from pushover import PushoverClient
import os, sys

if __name__ == '__main__':

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', dest='host', default="localhost", help='MQTT host send results to')
    parser.add_argument('-t', dest='topic', default="", help='MQTT topic to process')
    parser.add_argument('-m', dest='message', default="", help='MQTT message to process')

    args = parser.parse_args()
    #print args.host
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    #print "Path:"
    #print path 
    #print "___________"

    #Connecing to the specified host 
    client = mosquitto.Mosquitto("echo reactor")

    user = "driver"
    password = "1234"

    if user != None:
        client.username_pw_set(user,password)

    client.connect(args.host)

    PushClient = PushoverClient(path + "/" + "pushover.cfg")
    PushClient.send_message(args.message)

    keyword = args.topic.find("/send")

    #We need to be in the send path to send confirmation message. Avoids loops.
    if keyword == -1:
	exit(0)


    topic = args.topic[:keyword]


    #Echoing the message recived. 
    client.publish(topic, "Message sent!", 1)
    client.disconnect()

    
