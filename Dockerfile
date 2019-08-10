FROM ubuntu:18.04

RUN apt-get update -y

RUN apt-get install -y jq
RUN apt-get install -y python3.5
RUN apt-get install -y python3-pip

RUN pip3 install apache-beam==2.14.0
RUN pip3 install python-levenshtein==0.12.0
RUN pip3 install spacy==2.1.7

RUN python3 -m spacy download en_core_web_lg

ENV LANG C.UTF-8
