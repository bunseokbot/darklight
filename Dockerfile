FROM python:3-onbuild
MAINTAINER Namjun Kim <bunseokbot@gmail.com>

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libmysqlclient-dev libfontconfig

CMD ['python', 'run_sources.py']
