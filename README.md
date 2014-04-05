MQTT-Stage
==========

MQTT Stage produces and acts on MQTT messages by running a number of user defined or predefined python scripts. 

The scipts are divided into two types, actors and reactors. An actor script runns continously and produces MQTT scrips based om some hardware or webresource that it is connected to. An reactor is triggered to run each time a specific event is recieved. 

In hte MQTT stage directory there are three directories. One the actor directory the reactor directory and the topics directory. Whenever a new topic is recived over MQTT a folder path mathing the topic is created inside topics. 

To trigger a scprit a link from the reaktor script in the reactor folder to the path in topic can be created or a script can be directly placed inside the topic path. 

A reactor script
________________
The script need to be named NAME.react.py to be run as a reactor script. The script should have a react function. This function is called with the topic and the payload as parameters. 

An actor script 
________________
Should be named NAME.actor.py


The project is a work in progress state. Estimated alfa release is 24 of april. 
