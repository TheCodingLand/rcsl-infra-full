FROM ubuntu:bionic
RUN apt-get update && apt-get install -y \ 
    build-essential \
    python3 \
    python \
    python-dev \
    libxml2-dev \
    libxslt-dev \
    libssl-dev \
    zlib1g-dev \
    libyaml-dev \
    libffi-dev \
    python-pip \
    python3-pip

# General dev tools
RUN apt-get install -y git

# Latest versions of python tools via pip
RUN pip3 install --upgrade pip \ 
                         virtualenv \
                          requests
# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements (to leverage Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt

# install requirements


# add app


RUN apt-get update
RUN apt-get -y install firefox
RUN apt-get -y install wget
RUN apt-get -y install python3.6
#RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.20.1/geckodriver-v0.20.1-linux64.tar.gz
RUN tar -xvzf geckodriver-v0.20.1-linux64.tar.gz
RUN chmod +x geckodriver
RUN mv geckodriver /usr/local/bin/

ADD . /usr/src/app
RUN pip3 install -r requirements.txt
CMD python3 ./main.py