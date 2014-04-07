MQTT-Stage
==========

MQTT Stage produces and acts on MQTT messages by running a number of user defined or predefined python scripts. 

The scipts are divided into two types, actors and reactors. An actor script runns continously and produces MQTT messages based om some hardware or webresource that it is connected to. An reactor is triggered to run each time a specific event is recieved. 

In the MQTT stage directory there are three directories. One the actors directory the reactors directory and the topics directory. Whenever a new topic is recived over MQTT a folder path mathing the topic is created inside topics. 

To trigger a scrit place it inside the topic path or create a sympolic link into the path. The script will be started on the first message with the topic maching the script path.  

Example of link 
> ln -s ~/MQTT-Stage/reactors/writeDB.py /MQTT-Stage/topics/myhome/livingroom/temp/updatedatabase.react.py

This will cause the script writeDB to be run whenever we recive a message with the topic: /myhome/livingroom/temp

Scripts needs to be exeutable in order to run.


A reactor script
________________
The script need to be named NAME.react.py to be run as a reactor script. The script will be called with the same parameter set as the mosquitto_pub command. 

An actor script 
________________
Should be named NAME.actor.py 
The actor scripts are started immediatly if they are linked or placed in the actor/run-always folder. 
The are otherwise started on the first message mathching the path. 


The project is a work in progress state. Estimated alfa release is 24 of april. 
