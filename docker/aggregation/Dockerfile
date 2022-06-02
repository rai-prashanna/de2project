FROM python:3.8.10
RUN mkdir -p /app
ADD requirements.txt /app 
RUN cd /app
RUN pip install -r /app/requirements.txt --user --no-cache-dir
COPY ./agg-server.py /app
RUN chmod +x /app/agg-server.py
WORKDIR /app
CMD ["sleep 90"]



