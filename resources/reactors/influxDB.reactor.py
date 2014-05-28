#!/usr/bin/python 

# This script is ment to be used with MQTTstage and will send MQTT messages to an influxDB database.

from influxdb import client as influxdb
import argparse
import mosquitto
import os, sys
import json
import ConfigParser



if __name__ == '__main__':

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', dest='host', default="localhost", help='MQTT host send results to')
    parser.add_argument('-t', dest='topic', default="", help='MQTT topic to process')
    parser.add_argument('-m', dest='message', default="", help='MQTT message to process')

    args = parser.parse_args()

    #Where am I
    path = os.path.abspath(os.path.dirname(sys.argv[0]))

    #Load config file...

    ConfigFile = path + "/influxDB.cfg"
    
    #print "******DEBUG*******"
    #print ConfigFile 

    try:
        f = open(ConfigFile,"r")
        f.close()
    except:
        print "Please provide a valid config file! In the same folder as the couchDB script!"
        exit(1)
    
    #Read config file.    
    configfile = ConfigParser.RawConfigParser(allow_no_value=True)
    configfile.read(ConfigFile)


    #Load basic config.

    host = configfile.get("influxDB","host")
    port = configfile.get("influxDB","port")
    username = configfile.get("influxDB","user")
    password = configfile.get("influxDB","password")
    database = configfile.get("influxDB","database")
    

    if args.message[0] == '"':
	args.message = args.message[1:]
    if args.message[-1] == '"':
        args.message = args.message[:-1]

    data = json.loads(args.message)

    #Remove trailing slash
    #if args.topic[-1] == "/":
    #	topic = args.topic[:-1]
    #else:
    #	topic = args.topic
    	
    #field = topic.split("/")[-1].lower()
    
    db = influxdb.InfluxDBClient(host, port, username, password, database)
    
    data = [
    	{"points":[[data["time"],data["value"]],
   	 "name":topic,
         "columns":["time", "value"]
  	}]
    
    db.write_points(data)
    


    
