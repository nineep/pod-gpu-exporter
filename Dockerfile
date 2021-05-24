FROM python:3-alpine

ADD requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

ADD gpu-pod-exporter-unrestraint.py /opt/gpu-pod-exporter/gpu-pod-exporter.py

CMD python3 /opt/gpu-pod-exporter/gpu-pod-exporter.py
