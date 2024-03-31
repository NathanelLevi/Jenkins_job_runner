FROM python:3.9 AS builder
ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENV PYTHONPATH /app
CMD ["python", "/app/src/run_jenkins_job.py"]