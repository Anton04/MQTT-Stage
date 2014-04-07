#!/usr/bin/python 

import argparse
import mosquitto



if __name__ == '__main__':

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', dest='host', default="localhost", help='MQTT host send results to')
    parser.add_argument('-t', dest='topic', default="", help='MQTT topic to process')
    parser.add_argument('-m', dest='message', default="", help='MQTT message to process')

    args = parser.parse_args()
    #print args.host

    #Only act on PING messages!
    if args.message != "PING!":
	exit(0)

    #Connecing to the specified host 
    client = mosquitto.Mosquitto("echo reactor")

    user = "driver"
    password = "1234"

    if user != None:
        client.username_pw_set(user,password)

    client.connect(args.host)

    #Echoing the message recived. 
    print "Sending PONG!"
    client.publish(args.topic, "PONG!", 1)
    client.disconnect()

