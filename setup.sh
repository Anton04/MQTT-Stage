#!/bin/sh

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

sudo cp $DIR/MQTTstage.py /usr/bin/mqtt-stage

mkdir ~/MQTT-Stage

initctl reload-configuration

start mqtt-stage





