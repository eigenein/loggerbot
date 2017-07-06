FROM ubuntu:17.04
MAINTAINER Pavel Perestoronin <eigenein@gmail.com>

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt update && apt -y install git-core python3.6 python3-pip

COPY . /opt/loggerbot
WORKDIR /opt/loggerbot

RUN python3.6 -m pip install -r requirements.txt

RUN mkdir -p /srv/loggerbot
VOLUME /srv/loggerbot

CMD ["python3.6", "bot.py", "/srv/loggerbot/loggerbot.sqlite3"]
