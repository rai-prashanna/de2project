FROM python:3.7.13-bullseye
RUN mkdir -p /app
ADD requirements.txt /app 
RUN cd /app
RUN pip install -r /app/requirements.txt --user --no-cache-dir
COPY ./request-producer.py /app
RUN chmod +x /app/request-producer.py
WORKDIR /app
CMD /usr/local/bin/python /app/request-producer.py
