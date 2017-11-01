FROM python:2.7

MAINTAINER Anton Gustafsson  <anton.gustafsson@ri.se>

#RUN apt-get update

##################################################
# Set environment variables                      #
##################################################



##################################################
# Add app user                                   #
##################################################

#RUN useradd --create-home --home-dir /home/app --shell /bin/bash app


##################################################
# Install tools                                  #
##################################################
RUN pip install paho-mqtt 




#####SPECIFIC#####

USER root


#EXPOSE 

COPY MQTTstage.py MQTTstage.py 


CMD [ "python","./MQTTstage.py" ]
