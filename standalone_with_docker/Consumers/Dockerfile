FROM python:3.9-buster
ADD requirements.txt q1-consumer.py ./ 
RUN pip install -r requirements.txt
CMD ["sleep 121"]
ENTRYPOINT ["python"]
CMD ["./q1-consumer.py", "10"]
