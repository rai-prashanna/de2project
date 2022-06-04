FROM python:3.7.13-bullseye
RUN mkdir -p /app
ADD requirements.txt /app 
RUN cd /app
RUN pip install -r /app/requirements.txt --user --no-cache-dir
COPY q1-consumer.py /app
COPY q2-consumer.py /app
COPY q3-consumer.py /app
COPY q4-consumer.py /app

CMD ["sleep 60"]


