#!/usr/bin/python

# By Anton Gustafsson
# 2014-04-05

import os 
import sys

class MQTTstage():
  def __init__(self,path):
	
    if path.find("~") != -1:
    	path = os.path.expanduser(path)

    if not (self.CheckDirectories(path)):
      raise Exception("Can't initialize directorires!")
    self.basepath = path
    
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

if __name__ == '__main__':

  #Use default path if no argument given. 
  if len(sys.argv) == 1:
    BASEPATH = "~/MQTT-Stage"
  else:
    BASEPATH = sys.argv[1]

  print "Lanching MQTT stage at " + BASEPATH
  
  Stage = MQTTstage(BASEPATH)   
