FROM python:3.6.1

# Initialize
RUN mkdir -p /data/pdflist
WORKDIR /data/pdflist

# Setup

COPY requirements.txt /data/pdflist/
RUN pip3 install -r requirements.txt

#saving build time


# Prepare
COPY . /data/pdflist/

RUN mkdir -p mydjango/static/admin