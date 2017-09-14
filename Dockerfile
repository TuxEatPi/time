FROM tuxeatpi/common
  
COPY dialogs /dialogs
COPY intents /intents

COPY test_requirements.txt /opt/test_requirements.txt
COPY requirements.txt /opt/requirements.txt

RUN sed -i 's/.*python-aio-etcd.*//' /opt/requirements.txt && \
    sed -i 's/.*tuxeatpi-common.*//' /opt/requirements.txt

COPY setup.py /opt/setup.py
COPY tuxeatpi_time /opt/tuxeatpi_time
RUN cd /opt && python /opt/setup.py install

CMD ["time"]

