#!/bin/sh

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#Copy exe file
sudo cp $DIR/MQTTstage.py /usr/bin/mqtt-stage

#Copy upstart job
#sudo cp $DIR/upstart.sh.conf /etc/init/mqtt-stage.conf


mkdir ~/MQTT-Stage

#sudo initctl reload-configuration

#start mqtt-stage





