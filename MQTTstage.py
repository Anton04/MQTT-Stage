#!/usr/bin/python

# By Anton Gustafsson
# 2014-04-05

import os 
import sys
import subprocess
from time import sleep
import time  
import mosquitto
import thread

PORT = '/dev/ttyUSB0'
PREFIX = "rfxcom"
MQTT_HOST = "localhost"
TOPIC = "#"

class MQTTstage(mosquitto.Mosquitto):
	def __init__(self,path,ip = "localhost", port = 1883, clientId = "MQTTstage", user = "driver", password = "1234", topic = "#"):

		mosquitto.Mosquitto.__init__(self,clientId)

		self.output_subs = True
		self.debugsubs = True

		self.prefix = "MQTTStage"
				
		self.topic = topic
		
		if path.find("~") != -1:
			path = os.path.expanduser(path)

		if not (self.CheckDirectories(path)):
			raise Exception("Can't initialize directories!")
		#self.basepath = path
		
		self.ip = ip
		self.port = port
		self.clientId = clientId
		self.user = user
		self.password = password

		self.processes = {}
		self.running = {}
		
		if user != None:
			self.username_pw_set(user,password)

		self.will_set( topic =  "system/" + self.prefix, payload="Offline", qos=1, retain=True)


		print "Connecting"
		self.connect(ip)
		self.subscribe(self.topic, 0)
		self.on_connect = self.X_on_connect
		self.on_message = self.X_on_message

		#thread.start_new_thread(self.ControlLoop2,())
		self.loop_start()

		return
		
	def X_on_connect(self, selfX,mosq, result):
		print "MQTT connected!"
		self.publish(topic = "system/"+ self.prefix, payload="Online", qos=1, retain=True)
		self.subscribe(self.topic, 0)
		
	def X_on_message(self, selfX,mosq, msg):
		#try:
		if True:
			print("RECIEVED MQTT MESSAGE: "+msg.topic + " " + str(msg.payload))
			topics = msg.topic.split("/")

			path = self.topics_path + msg.topic

			if path[-1] != "/":
				path += "/"

			#Create directory
			if self.CheckPath(path):    	
				self.StartScrips(path,reactors=True,recursive=False,topic = msg.topic,message = str(msg.payload))
		
			#Also run files in parent directories   
			for f in range(len(path)-2,len(self.topics_path)-2,-1):
				if path[f] != "/":
					continue
				
				#print path[:f+1]
				self.StartScrips(path[:f+1],reactors=True,recursive=False,topic = msg.topic,message = str(msg.payload)) 
			
		#except:
		#print "Error when parsing incomming message."
		return
		
	def ControlLoop(self):
		# schedule the client loop to handle messages, etc.

		while True:
			#Check if new actors has been added. 
			self.StartActors()
			self.UnloadRemovedScripts()
			sleep(10)


	def CheckPath(self,path,Autocreate=True):

		#Check full path
		if self.CreateDirectory(path):
			 return True

		#If we fail check dir by dir.
		dirs = path.split("/")

		subpath = ""

		for dir in dirs:	
			subpath += dir + "/"

			print "Testing: " + subpath

			if not self.CreateDirectory(subpath):
				return False
		
		return True
				
		
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
		self.StartScrips(self.actors_run_always)

	def StartScrips(self,path,reactors=False,recursive=False,topic = None,message = None):
		
		#List all the files in the current folder. 
		tree = os.walk(path)
		(dirpath, dirnames, filenames) = tree.next()
		
		#Check for scripts. 
		for file in filenames:
			#if file[-3:] != ".py"
			if not self.is_exe(dirpath + "/" + file):
					continue
	
			#Is actor
			is_actor = file.find(".actor") != -1
			is_reactor = file.find(".reactor") != -1

			#If we are running reactors make sure it is one. 
			if is_reactor and not reactors:
					continue

			#If its an actor and this call was made for triggering a reactor ignore it. 
			if is_actor and reactors:
					continue

			restart=False
			
			#Already started? 
			running = self.running.copy()
			if file in running:
					#Yes. Check if running.
					if running[file][0].poll() is None:
						#Still running
						if is_actor:
					 		continue
					else:
						try:
							del self.running[file]
						except KeyError:
							pass
						if is_actor:
							print file + " terminated. "
							restart = True	


			#Add parameters.
			param = []
			param.append("-h")
			param.append(self.ip)
			
			if topic:
					param.append("-t")
					param.append(topic)
			if message:
					param.append("-m")
					param.append("\"" + message + "\"")
			

			command = [dirpath + file] + param  # the shell command
			commandline = " ".join(command)

			if restart:
				print "Restarting actor script: " + commandline
			elif is_actor:
				print "Starting actor script: " + commandline
			else:
				print "Triggering reactor script: " + commandline

			#if self.debugfiles:
			#    errorfile = open(dirpath + file + ".err.log","w")
			#    stdoutfile = open(dirpath + file + ".out.log","w")
			#else:
					#    errorfile = open("/dev/null","w")
						#    stdoutfile = open("/dev/null","w")

			if self.output_subs:
				process = subprocess.Popen(command, stdout=sys.stdout,stderr=sys.stderr, shell=False)
			else:
				if self.debugsubs:
					outfile = open(os.devnull, 'w')
				else:
					outfile = open(dirpath + file + ".log", 'w')
				process = subprocess.Popen(command, stdout=outfile,stderr=outfile, shell=False)

			#output, error = process.communicate()
							
			pid_nr = process.pid
			#TODO write pid to /running
							
			self.running[file] = [process,commandline] 
				
			#TODO also check subfolders if recursive

		return 

	def UnloadRemovedScripts(self):
	
		invalid = []

		#Local copy
		running = self.running.copy()

		#Unload removed scripts
		for file in running:
			try:
				os.stat(self.running[file][1].split(" ")[0])
			except:
				print file + " removed. Killing process..."
				running[file][0].kill()
				invalid.append(file)

		#Remove reference
		for file in invalid:	
			try:
				del self.running[file]
			except KeyError:
				pass

		#TODO also check subfolders if recursive

		
		return
		
	
	def killall(self):

		running = self.running.copy()
		#Kill all running subprocesses
		for item in running:
			running[item][0].kill()
		

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
	

		 
