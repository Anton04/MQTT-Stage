#!/usr/bin/python

# By Anton Gustafsson
# 2014-04-05

import os 
import sys
import subprocess

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
    
    return
    
  def CreateDirectory(self,path):
    #Create directories
    try:
      print "Checking " + path
      os.stat(path)
    except:
      try:
	print "Creating " + path
        os.mkdir(path)
        return True
      except:
	print "Failed ot create " + path 
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
    
    paths = [self.basepath,self.topics, self.actors, self.reactors]
    
    n = 0

    #Create all dirs
    for directory in paths:
      n += self.CreateDirectory(directory)
      
    #Check if we all went well. 
    if n == len(paths):
	return True
    else: 
	return False  

  def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

  def StartActors(self):
  	
    #List all the files in the actors folder. 
    tree = os.walk(self.actors)
    (dirpath, dirnames, filenames) = tree.next()
    
    ScriptsToRun = []
    
    #Check wich ones to that are scrips. 
    for file in filenames:
    	#if file[-3:] != ".py"
    	if not self.is_exe(dirpath + "/" + file):
    		continue
    	
    	#Check for pid. 
    	try:
    	    pid = open(self.pid + "/" + file + ".pid","r")
    	    pid_nr = pid.readline()
    	    cmd = open("/proc/%s/cmdline" % pid_nr).readline()
    	    if cmd.find(dirpath + "/" + file) == -1
    	    	raise NameError('Not matching command')
    	    	
    	except:
    	    try:	
    	    	del self.processes[pid_nr]
    	    except:
    	    	pass
    	    print "No pid found. Starting: " + file
    	    #Run as external process 
    	    command = dirpath + "/" + file   # the shell command
    	    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    	    output, error = process.communicate()
    	    
    	    pid_nr = process.pid
    	    
    	    pid = open(self.pid + "/" + file + ".pid","w")
    	    pid.write(pid_nr)
    	    
    	    pid.close()
    	    
    	self.processes[pid_nr] = [command, process, output, error] 
    	    
    

    #TODO also check subfolders
    
    return
    
	

for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(filenames)
    break
  	

if __name__ == '__main__':

  #Use default path if no argument given. 
  if len(sys.argv) == 1:
    BASEPATH = "~/MQTT-Stage"
  else:
    BASEPATH = sys.argv[1]

  print "Lanching MQTT stage at " + BASEPATH
  
  Stage = MQTTstage(BASEPATH)   
