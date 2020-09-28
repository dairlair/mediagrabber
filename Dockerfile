FROM python:3.8.6-slim-buster

COPY install-packages.sh .
RUN chmod +x ./install-packages.sh
RUN ./install-packages.sh

WORKDIR /mediagrabber

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

ADD requirements.txt /mediagrabber/requirements.txt
RUN pip install -r requirements.txt

ADD . /mediagrabber
RUN pip install -e .

ENV CORE_WORKDIR=/tmp
ENV AMQP_URL=amqp://guest:guest@host.docker.internal:5672/%2F
ENV AMQP_IN=mediagrabber.in
ENV AMQP_OUT=mediagrabber.out


ENV PYTHONUNBUFFERED=1

CMD ["python", "mediagrabber/amqp.py"]