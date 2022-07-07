FROM python:3.9
MAINTAINER Jean

# Update Container
# update aptitude and install git (maybe cron)
RUN apt-get update && apt-get install -y git
# update pip3
RUN python3 -m pip install --upgrade pip

# create a (work)dir and set it for all the subsequent dockerfile instruction
RUN mkdir /opt/bot/
WORKDIR /opt/bot/

# github token
ARG TOKEN=INSERT_TOKEN_HERE

# clone the actual repository (don't forget ".")
RUN git clone https://$TOKEN@github.com/JeanS-github/GCC-bot .

# add the cronjob script
#RUN bash addcron.sh
#initially this script (that I never wrote) was here to automatically pull
#the python script from github, and run the newer version 
#(without stopping, pulling, and running again the docker container)

# install the requirements 
RUN pip3 install -r requirements.txt
# launch python script
RUN python3 main.py
# other way to run script
#CMD ["python3", "./main.py"]
