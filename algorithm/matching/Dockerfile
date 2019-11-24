FROM ubuntu:latest

MAINTAINER Jihyeok Yang <flash3470@gmail.com>

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install build-essential ssh -y
RUN apt-get install python -y
RUN apt-get install vim -y
RUN apt-get install net-tools -y
RUN apt-get install python-pip -y
RUN apt-get install python3-pip -y
RUN pip install pymongo
RUN pip3 install pymongo
RUN pip3 install pandas
RUN pip3 install matplotlib
RUN pip3 install numpy
RUN pip3 install scipy

WORKDIR /root/
COPY entry_shell.sh entry_shell.sh
RUN chmod 777 entry_shell.sh

COPY TemplateList.py TemplateList.py

RUN mkdir stdlog
COPY stdlog/ stdlog/

COPY matching.py matching.py
ENTRYPOINT bash -C './entry_shell.sh';'bash'
