#!/usr/bin/python 

import argparse
import mosquitto
#from pushover import PushoverClient
import os, sys
import urllib2
import json, base64

#Posting data to couchDB  
def post(doc):

	global config

	url = 'http://%(server)s/%(database)s/_design/energy_data/_update/measurement' % config
#	print url
	request = urllib2.Request(url, data=json.dumps(doc))
	auth = base64.encodestring('%(user)s:%(password)s' % config).replace('\n', '')
	request.add_header('Authorization', 'Basic ' + auth)
	request.add_header('Content-Type', 'application/json')
	request.get_method = lambda: 'POST'
	urllib2.urlopen(request, timeout=1)

	return

if __name__ == '__main__':

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', dest='host', default="localhost", help='MQTT host send results to')
    parser.add_argument('-t', dest='topic', default="", help='MQTT topic to process')
    parser.add_argument('-m', dest='message', default="", help='MQTT message to process')

    args = parser.parse_args()

    #Where am I
    path = os.path.abspath(os.path.dirname(sys.argv[0]))

    #Load config file...

    ConfigFile = path + "/couchm.cfg"

    try:
        f = open(ConfigFile,"r")
        f.close()
    except:
        print "Please provide a valid config file! In the same folder as the couchDB script!"
        exit(1)
    
    #Read config file.    
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read(ConfigFile)


    #Load basic config.

    config = {}
    config["user"] = config.get("CouchDB","user")
    config["password"] = config.get("CouchDB","password")
    config["server"] = config.get("CouchDB","server")
    config["database"] = config.get("CouchDB","database")
    
    source = config.get("CouchM","source")
    

    if args.message[0] == '"':
	args.message = args.message[1:]
    if args.message[-1] == '"':
        args.message = args.message[:-1]

    data = json.loads(args.message)
    
    #Post data to couchm
    post({
                        	"source": source,
	                        "timestamp": str(data["time"]),
	                        "ElectricPower": str(data["value"]),
	                        "ElectricEnergy": str(0),
	                        "PowerThreshold": str(1),
				"ElectricPowerUnoccupied": "0",
				"ElectricEnergyOccupied": "0",
				"ElectricEnergyUnoccupied": "0"
                        })


    
