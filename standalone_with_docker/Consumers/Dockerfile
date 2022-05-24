FROM python:3.9-alpine
RUN mkdir -p /app
ADD requirements.txt /app 
RUN cd /app
RUN pip install -r /app/requirements.txt 
EXPOSE 6650
