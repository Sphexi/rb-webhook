FROM python:3.7-buster
COPY . /app
CMD python /app/webhook-main.py