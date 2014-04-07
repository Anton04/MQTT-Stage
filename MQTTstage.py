#!/usr/bin/python

# By Anton Gustafsson
# 2014-04-05

import os 
import sys
import subprocess
from time import sleep 
import mosquitto

PORT = '/dev/ttyUSB0'
PREFIX = "rfxcom"
MQTT_HOST = "localhost"
TOPIC = "#"

class MQTTstage(mosquitto.Mosquitto):
  def __init__(self,path,ip = "localhost", port = 1883, clientId = "MQTTstage", user = None, password = None, topic = "#"):

    mosquitto.Mosquitto.__init__(self,clientId)
    
    self.topic = topic
    
    if path.find("~") != -1:
    	path = os.path.expanduser(path)

    if not (self.CheckDirectories(path)):
      raise Exception("Can't initialize directorires!")
    self.basepath = path
    
    self.ip = ip
    self.port = port
    self.clientId = clientId
    self.user = user
    self.password = password

    self.processes = {}
    self.running = {}
    
    if user != None:
    	self.username_pw_set(user,password)

    print "Connecting"
    print self.connect(ip)
    #self.subscribe(self.topic, 0)
    self.on_connect = self.X_on_connect
    self.on_message = self.X_on_message

    return
    
  
    
  def X_on_connect(self, selfX,mosq, result):
    print "MQTT connected!"
    self.subscribe(self.topic, 0)
    
  def X_on_message(self, selfX,mosq, msg):
    #try:
    if True:
    	print("RECIEVED MQTT MESSAGE: "+msg.topic + " " + str(msg.payload))
    	topics = msg.topic.split("/")

	#Create directory
	self.CreateDirectory(self.topics_path + msg.topic)    	

    #except:
#	    print "Error when parsing incomming message."
    return
    
  def ControlLoop(self):
    # schedule the client loop to handle messages, etc.
    print "Starting MQTT listener"
    while True:
    	self.StartActors()
        sleep(0.1)
        
        self.loop(10000)
        #Check if new actors has been added. 

    
  def CreateDirectory(self,path):
    #Create directories
    try:
      #print "Checking folder: " + path
      os.stat(path)
    except:
      try:
	print "Creating folder: " + path
        os.mkdir(path)
        return True
      except:
	print "Failed to create: " + path 
        return False 
    
    return True

  #Make sure we gave the directories we need. 
  def CheckDirectories(self,path):
    
    if path[-1] != "/":
      path = path + "/"
    
    #Create directories
    self.basepath = path
    self.topics_path = path + "topics/"
    self.actors = path + "actors/"
    self.actors_run_always = path + "actors/run-always/"
    #self.pid = path + "actors/running"
    self.reactors = path + "reactors/"
    
    paths = [self.basepath,self.topics_path, self.actors, self.reactors,self.actors_run_always]
    
    n = 0

    #Create all dirs
    for directory in paths:
      n += self.CreateDirectory(directory)
      
    #Check if we all went well. 
    if n == len(paths):
	return True
    else: 
	return False  

  def is_exe(self,fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

  def StartActors(self):
  	
    #List all the files in the actors folder. 
    tree = os.walk(self.actors)
    (dirpath, dirnames, filenames) = tree.next()
    
    #ScriptsToRun = []
    #print "Checking actor scripts!"	
    
    #Check for actor scripts. 
    for file in filenames:
    	#if file[-3:] != ".py"
    	if not self.is_exe(dirpath + "/" + file):
    		continue
	if file.find(".actor") == -1:
		continue

	restart=False
	
	#Already started? 
	if file in self.running:
	    #Yes. Check if running.
	    if self.running[file][0].poll() is None:
		#Still running
		continue
	    else:
	 	del self.running[file]
		print file + " terminated. "
		restart = True	

    	command = dirpath + file   # the shell command

	if restart:
	    print "Restarting script: " + command
	else:
	    print "Starting script: " + command 
    	process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    	#output, error = process.communicate()
	#print "stuck here"
    	    
    	pid_nr = process.pid
	#TODO write pid to /running
    	    
	self.running[file] = [process,command] 
    	
    invalid = []

    #Unload removed scripts    
    for file in self.running:
	if file not in filenames:
	    print file + " removed. Killing process..."
	    self.running[file][0].kill()
	    invalid.append(file)

    #Remove reference
    for file in invalid:	
    	del self.running[file]

    #TODO also check subfolders

    
    return
    
	
  def killall(self):
    #Kill all running subprocesses
    for item in self.running:
	self.running[item][0].kill()
  	

  def __del__(self):
    self.killall()
    return

if __name__ == '__main__':

  #Use default path if no argument given. 
  if len(sys.argv) == 1:
    BASEPATH = "~/MQTT-Stage"
  else:
    BASEPATH = sys.argv[1]

  print "Lanching MQTT stage at " + BASEPATH
  
  Stage = MQTTstage(BASEPATH)   

  #try:
  if True:
      while(True):
          Stage.ControlLoop()
          sleep(10)
 # except:
      Stage.killall()
	

     
