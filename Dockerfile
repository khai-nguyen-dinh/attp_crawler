# khainguyen
# Dockerfile
#
FROM ubuntu:14.04
MAINTAINER khainguyen "khainguyenptiter@gmail.com"

RUN apt-get update

RUN apt-get install -y gcc g++ python-dev libssl-dev libxml2-dev libxslt1-dev libffi-dev libmysqlclient-dev python-pip python-mysqldb
RUN apt-get install -y libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
COPY requirements.txt /
RUN pip install -r /requirements.txt

