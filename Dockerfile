FROM google/debian:wheezy

RUN apt-get update -y && \
    apt-get install --no-install-recommends -y -q build-essential python2.7 python2.7-dev python-pip git
RUN pip install -U pip
RUN pip install virtualenv

WORKDIR /app
ONBUILD RUN virtualenv /env
ONBUILD ADD requirements.txt /app/requirements.txt
ONBUILD RUN /env/bin/pip install -r /app/requirements.txt
ONBUILD ADD . /app

EXPOSE 8080
CMD []
ENTRYPOINT ["/env/bin/python", "main.py"]