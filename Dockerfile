FROM python:3.5-alpine

#RUN apk add --no-cache git gcc python-dev linux-headers musl-dev
RUN apk add --no-cache git gcc python-dev musl-dev

WORKDIR /opt
COPY requirements.txt /opt/requirements.txt
COPY test_requirements.txt /opt/test_requirements.txt
RUN pip install -r /opt/requirements.txt

RUN mkdir -p /workdir

COPY setup.py /opt/setup.py
COPY tuxeatpi_time /opt/tuxeatpi_time

RUN python /opt/setup.py install

COPY dialogs /dialogs
COPY intents /intents

WORKDIR /workdir

ENTRYPOINT ["tep-time", "-w", "/workdir", "-I", "/intents", "-D", "/dialogs"]
