#!/usr/bin/python 

import argparse
import mosquitto
#from pushover import PushoverClient
import os, sys
import urllib2
import json, base64
import ConfigParser

#Posting data to couchDB  
def post(doc):

	global config

	url = 'http://%(server)s/%(database)s/_design/energy_data/_update/measurement' % config


	#print "********DEBUG********"
	#print config
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

    config = {}
    config["user"] = configfile.get("CouchDB","user")
    config["password"] = configfile.get("CouchDB","password")
    config["server"] = configfile.get("CouchDB","server")
    config["database"] = configfile.get("CouchDB","database")
    
    source = configfile.get("CouchM","source")
    

    if args.message[0] == '"':
	args.message = args.message[1:]
    if args.message[-1] == '"':
        args.message = args.message[:-1]

    data = json.loads(args.message)

    #Remove trailing slash
    if args.topic[-1] == "/":
    	topic = args.topic[:-1]
    else:
    	topic = args.topic
    	
    field = topic.split("/")[-1].lower()
    
    
    if "value" in data:
    	#Assume power stream only.	
    	
    	#Interpolate energy counter 
    	try:
    		#Read from file
    		file = open(path + "/couchm.context","r")
    		
    		MeterEvent = json.load(file)
    		file.close()
    		
    		#THIS NEEDS TO BE CHANGED TO MS in other scripts. i.e. 3600000.0
    		deltaT = (data["time"] - MeterEvent["time"])/3600.0
    		
    		MeterEvent["energy"] += (MeterEvent["power"] * deltaT) 
    		MeterEvent["power"] = data["value"]
    		MeterEvent["time"] = data["time"]
    		
    	#Or create new
    	except:
    		print "DEBUG:  Creating first MeterEvent"
    		MeterEvent = {}
    		MeterEvent["time"] = data["time"]
    		MeterEvent["power"] = data["value"]
    		MeterEvent["energy"] = 0.0
    		MeterEvent["threshold"] = 1.0
    	
    	#Save
    	try:
    		file = open(path + "/couchm.context","w")
    		json.dump(MeterEvent,file)
    		file.close()
    	except:
    		print "CouchM reactor: Unable to save context!"
    		
    	power = MeterEvent["power"]
    	energy_counter = MeterEvent["energy"]
        power_threshhold = MeterEvent["threshold"]
        
    elif "threshold" in data:
    	#Assume meterevent
    	power = data["power"]
    	energy_counter = data["energy"]
        power_threshhold = data["threshold"]
    else:
    	print "CouchM reactor: Unable to interpret data"
    	exit(0)
    
    #Post data to couchm
    post({
                        	"source": source,
	                        "timestamp": str(data["time"]),
	                        "ElectricPower": str(power),
	                        "ElectricEnergy": str(energy_counter),
	                        "PowerThreshold": str(power_threshhold),
				"ElectricPowerUnoccupied": "0",
				"ElectricEnergyOccupied": "0",
				"ElectricEnergyUnoccupied": "0"
                        })


    
