FROM rocketchat/hubot-rocketchat
USER root
RUN \
  apt-get update && \
  apt-get install -y python python-dev python-pip python-virtualenv && \
  rm -rf /var/lib/apt/lists/*
RUN pip install requests
USER hubot