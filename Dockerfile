FROM python:3.9 AS builder
ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt

# A distroless container image with Python and some basics like SSL certificates
# https://github.com/GoogleContainerTools/distroless
FROM python:3.9
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["python /app/src/run_jenkins_job.py"]