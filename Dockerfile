FROM dairlair/mediagrabber-base:0.2.0

COPY install-packages.sh .
RUN chmod +x ./install-packages.sh
RUN ./install-packages.sh

WORKDIR /mediagrabber

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt


COPY . /mediagrabber
RUN pip install -e .

ENV LOG_LEVEL=WARNING
ENV WORKDIR=/tmp
ENV AMQP_URL=amqp://guest:guest@host.docker.internal:5672/%2F
ENV AMQP_IN=mediagrabber.in
ENV AMQP_OUT=mediagrabber.out


ENV PYTHONUNBUFFERED=1

CMD ["python", "mediagrabber/amqp.py"]