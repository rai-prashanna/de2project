FROM python:3.9-buster
ADD requirements.txt q1-producer.py ./ 
RUN pip install -r requirements.txt
CMD ["sleep 120"]
ENTRYPOINT ["python"]
CMD ["./q1-producer.py", "user", "token"]
