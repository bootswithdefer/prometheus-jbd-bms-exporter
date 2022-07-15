FROM python:3-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt
ADD python_jbdtool_bms python_jbdtool_bms

COPY prometheus-jbd-exporter.py .

CMD [ "python3", "prometheus-jbd-exporter.py" ]
