#!/usr/bin/python

# By Anton Gustafsson
# 2014-04-05

import os 
import sys

class MQTTstage():
  def __init__(self,path):
    if not (self.CheckDirectories(path)):
      raise Exception("Can't initialize directorires!")
    self.basepath = path
    
  def CreateDirectory(self,path):
        #Create directories
    try:
      os.stat(dir)
    except:
      try:
        os.mkdir(dir)
        return True
      except:
        return False 
    
    return True

  #Make sure we gave the directories we need. 
  def CheckDirectories(self,path):
    
    if path[-1] != "/":
      path = path + "/"
    
    #Create directories
    self.topics = path + "topics/"
    self.actors = path + "actors/"
    self.reactors = path + "reactors/"
    
    paths = [self.topics, self.actors, self.reactors]
    
    for directory in paths:
      self.CreateDirectory(directory)
      
      

if __name__ == '__main__':

  #Use default path if no argument given. 
  if len(sys.argv) == 0:
    BASEPATH = "~/MQTT-Stage"
  else:
    BASEPATH = sys.argv[0]

  print "Lanching MQTT stage at " + BASEPATH
  
  Stage = MQTTStage(BASEPATH)   
