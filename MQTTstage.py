#!/usr/bin/python

# By Anton Gustafsson
# 2014-04-05

import os 
import sys
import subprocess
from time import sleep 

class MQTTstage():
  def __init__(self,path,ip = "localhost", port = 1883, clientId = "MQTTstage", user = None, password = None):
	
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
    
    return
    
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
    self.topics = path + "topics/"
    self.actors = path + "actors/"
    self.pid = path + "actors/running"
    self.reactors = path + "reactors/"
    
    paths = [self.basepath,self.topics, self.actors, self.reactors,self.pid]
    
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
          Stage.StartActors()
          sleep(10)
 # except:
      Stage.killall()
	

     
