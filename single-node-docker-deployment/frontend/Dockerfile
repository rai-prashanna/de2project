<<<<<<< HEAD
FROM python:3.7.13-bullseye
RUN mkdir -p /app
ADD requirements.txt /app 
RUN cd /app
RUN pip install -r /app/requirements.txt --user --no-cache-dir
COPY ./ /app
RUN chmod +x /app/app.py
WORKDIR /app
CMD /usr/local/bin/python /app/app.py
=======
FROM python:3.6
ADD . /frontend
WORKDIR /frontend
RUN pip install -r requirements.txt
>>>>>>> 09be0480073c05b8bbf7d062187076936882ebf4
