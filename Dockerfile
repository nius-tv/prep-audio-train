FROM ubuntu:18.04

RUN apt-get update -y

RUN apt-get install -y python2.7
RUN apt-get install -y python-pip

RUN pip install apache-beam[gcp]==2.14.0
RUN pip install python-levenshtein==0.12.0
RUN pip install spacy==2.1.7

RUN python -m spacy download en_core_web_lg
